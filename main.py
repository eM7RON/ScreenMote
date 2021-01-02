#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import copy
import os
import subprocess
import sys
import time

from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5 import QtWidgets

from gui.main_window import Ui_MainWindow
from gui.confirmation_prompt import Ui_ConfirmationPrompt
from gui.login import Ui_Login

from common import constants as c
from common import utils


# Handle high dpi displays:
if hasattr(QtCore.Qt, "AA_EnableHighDpiScaling"):
    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
if hasattr(QtCore.Qt, "AA_UseHighDpiPixmaps"):
    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)


class AlignDelegate(QtWidgets.QStyledItemDelegate):
    def initStyleOption(self, option, index):
        super(AlignDelegate, self).initStyleOption(option, index)
        option.displayAlignment = QtCore.Qt.AlignCenter


class ScreenMote(QtWidgets.QWidget, Ui_MainWindow):
    """
    A window for managing asset updates
    """

    asset_queue = []

    def __init__(self, parent=None):
        super(ScreenMote, self).__init__(parent=parent)
        self.setupUi(self)
        self.setWindowIcon(c.ICON)

        self.confirm_update_prompt = ConfirmationPrompt(
            yes_action=self.execute_update, message="Execute update. Are you sure?"
        )
        self.confirm_reboot_prompt = ConfirmationPrompt(
            yes_action=lambda: power_cycle(self.read_host_table(), "reboot", password),
            message="Reboot. Are you sure?",
        )
        self.confirm_shutdown_prompt = ConfirmationPrompt(
            yes_action=lambda: power_cycle(
                self.read_host_table(), "shutdown", password
            ),
            message="Shutdown. Are you sure?",
        )

        # Asset queue
        # Set columns widths
        self.asset_table.setColumnWidth(0, 75)
        self.asset_table.setColumnWidth(1, 50)
        self.asset_table.setColumnWidth(2, 400)
        # Set column allignment
        delegate = AlignDelegate(self.asset_table)
        for i in range(3):
            self.asset_table.setItemDelegateForColumn(i, delegate)

        # Host table
        host_data = utils.open_google_sheet(c.GOOGLE_SHEET_NAME, c.DEFAULT_CREDS_PATH)
        # Need to set size of table otherwise the table is invisible
        self.host_table.setRowCount(len(host_data))
        self.host_table.setColumnCount(4)
        # Populate table with data

        for host in host_data:
            i, mac, ipv4 = int(host["#"]) - 1, host["Mac"], host["IPV4"]
            if not ipv4.strip():
                ipv4 = "None"
            checkbox = QtWidgets.QTableWidgetItem()
            checkbox.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
            checkbox.setCheckState(QtCore.Qt.Checked)
            self.host_table.setItem(i, 0, checkbox)
            self.host_table.setItem(i, 1, QtWidgets.QTableWidgetItem(str(i + 1)))
            self.host_table.setItem(i, 2, QtWidgets.QTableWidgetItem(mac))
            self.host_table.setItem(i, 3, QtWidgets.QTableWidgetItem(ipv4))

        # Center allign column's contents
        delegate = AlignDelegate(self.host_table)
        for i in range(4):
            self.host_table.setItemDelegateForColumn(i, delegate)

        # # Set column size to contents
        self.host_table.setColumnWidth(0, 60)
        self.host_table.setColumnWidth(1, 40)
        self.host_table.setColumnWidth(2, 148)
        self.host_table.setColumnWidth(3, 140)

        # For Validating inputs and identifying ready state

        # Controls that are checked
        self.asset_inputs = [self.name_line_edit, self.url_line_edit]
        for control in self.asset_inputs:
            control.valid = False
        # Controls that become unclocked when above are in valid states
        self.validated_asset_controls = [self.add_asset_button]

        # Controls that are checked
        self.update_inputs = [self.asset_table, self.host_table]
        for control in self.update_inputs:
            control.valid = False
        # Controls that become unclocked when above are in valid states
        self.validated_update_controls = [self.update_button]

        # Controls that are checked
        self.power_inputs = [self.host_table]
        for control in self.power_inputs:
            control.valid = False
        # Controls that become unclocked when above are in valid states
        self.validated_power_controls = [self.reboot_button, self.shutdown_button]

        self.name_line_edit.textChanged.connect(self.validate_name)
        self.url_line_edit.textChanged.connect(self.validate_url)
        self.add_asset_button.clicked.connect(self.queue_asset)
        self.asset_table.itemChanged.connect(self.validate_asset_table)
        self.host_table.itemChanged.connect(self.validate_host_table)
        self.update_button.clicked.connect(self.confirm_update_prompt.show)
        self.reboot_button.clicked.connect(self.confirm_reboot_prompt.show)
        self.shutdown_button.clicked.connect(self.confirm_shutdown_prompt.show)

        self.validate_name()
        self.validate_url()
        self.validate_asset_table()
        self.validate_host_table()

    def queue_asset(self):
        name = self.name_line_edit.text().strip()
        url = self.url_line_edit.text().strip()
        n_slides = self.n_slide_spin_box.value()

        row = self.asset_table.rowCount()
        self.asset_table.insertRow(row)
        self.asset_table.setItem(row, 0, QtWidgets.QTableWidgetItem(name))
        self.asset_table.setItem(row, 2, QtWidgets.QTableWidgetItem(url))
        self.asset_table.setItem(row, 1, QtWidgets.QTableWidgetItem(str(n_slides)))

        self.name_line_edit.setText("")
        self.url_line_edit.setText("")
        self.n_slide_spin_box.setValue(1)

    def validate_name(self):
        name = self.name_line_edit.text().strip()
        valid = bool(name)
        self.name_line_edit.valid = valid
        color = c.VALID_COLOR_MAP[valid]
        self.name_line_edit.setStyleSheet(f"QLineEdit {{ background-color: {color} }}")
        ready_check(self, self.validated_asset_controls, self.asset_inputs)

    def validate_url(self):
        url = self.url_line_edit.text().strip()
        empty = not bool(url)
        no_spaces = len(url.split(" ")) == 1
        isgoogle = url.startswith(r"https://docs.google.com/presentation/")
        isrepeated = url.count(r"https://docs.google.com/presentation/") > 1
        has_start = "start=true" in url
        has_loop = "loop=true" in url
        end_isnum = url.split("=")[-1].isnumeric()
        valid = all(
            [
                url,
                not empty,
                no_spaces,
                isgoogle,
                has_start,
                has_loop,
                end_isnum,
                not isrepeated,
            ]
        )
        self.url_line_edit.valid = valid
        color = c.VALID_COLOR_MAP[valid]
        self.url_line_edit.setStyleSheet(f"QLineEdit {{ background-color: {color} }}")
        ready_check(self, self.validated_asset_controls, self.asset_inputs)

    def validate_asset_table(self):
        valid = self.asset_table.rowCount() > 0
        self.asset_table.valid = valid
        ready_check(self, self.validated_update_controls, self.update_inputs)
        self.toggle_update_status_message()

    def toggle_update_status_message(self):
        valid = all([input_.valid for input_ in self.update_inputs])
        if valid:
            self.update_status_label.setText("Ready")
        else:
            self.update_status_label.setText("Not Ready")

    def toggle_power_status_message(self):
        valid = all([input_.valid for input_ in self.power_inputs])
        if valid:
            self.power_status_label.setText("Ready")
        else:
            self.power_status_label.setText("Not Ready")

    def validate_host_table(self):
        count = []
        for i in range(self.host_table.rowCount()):
            if self.host_table.item(i, 0).checkState():
                count.append(True)
        valid = any(count)
        self.host_table.valid = valid
        ready_check(self, self.validated_power_controls, self.power_inputs)
        self.toggle_update_status_message()
        self.toggle_power_status_message()

    def read_host_table(self):
        host_data = []
        for i in range(self.host_table.rowCount()):
            name = f"{c.HOST_NAME_TEMPLATE}{str(i).zfill(2)}"
            host = {
                "name": name,
                "mac": self.host_table.item(i, 2).text(),
                "ipv4": self.host_table.item(i, 3).text(),
                "enabled": bool(self.host_table.item(i, 0).checkState()),
            }
            host_data.append(host)
        return host_data

    def execute_update(self):
        self.confirm_update_prompt.close()
        names, n_slides, urls = asset_data = [[], [], []]
        for i in range(self.asset_table.rowCount()):
            for j in range(3):
                asset_data[j].append(self.asset_table.item(i, j).text())
        delete = self.delete_check_box.isChecked()
        host_data = self.read_host_table()
        update_assets(host_data, password, delete, names, urls, n_slides)
        self.status_update_label.setText("Done")


class ConfirmationPrompt(QtWidgets.QWidget, Ui_ConfirmationPrompt):
    """
    A generic window that can be used for multiple tasks. It prompts the user
    to make sure they want to do whatever they clicked on with "Are you sure?".
    Above this a custom message can be displayed by using the 'message' attribute.
    """

    def __init__(
        self, yes_action, no_action=None, window_title=None, message=None, parent=None
    ):
        super(ConfirmationPrompt, self).__init__(parent=parent)
        self.setupUi(self)
        self.setWindowIcon(c.ICON)
        if window_title is not None:
            self.setWindowTitle(window_title)

        self.message.setText(message if message is not None else "Continue?")

        self.yes_button.clicked.connect(yes_action)
        self.no_button.clicked.connect(
            no_action if no_action is not None else self.close
        )

        self.__show = copy.deepcopy(self.show)
        self.show = self._show

    def _show(self):
        """
        This method overwrites the built-in self.show method during __init__().
        It preserves the orginal self.show functionality but adds the ability
        position prompts at the position of the current main window
        """
        position_next_window(screenmote, self)
        self.__show()


class LoginPortal(QtWidgets.QWidget, Ui_Login):
    """
    A generic window that can be used for multiple tasks. It prompts the user
    to make sure they want to do whatever they clicked on with "Are you sure?".
    Above this a custom message can be displayed by using the 'message' attribute.
    """

    def __init__(self, parent=None):
        super(LoginPortal, self).__init__(parent=parent)
        self.setupUi(self)
        self.setWindowIcon(c.ICON)
        center_window(self)

        self.login_inputs = [self.password_line_edit]
        for control in self.login_inputs:
            control.valid = False
        self.validated_login_controls = [self.login_button]

        self.password_line_edit.textChanged.connect(self.validate_input)
        self.login_button.clicked.connect(self.validate_password)
        self.password_line_edit.returnPressed.connect(self.validate_password)
        self.validate_password()

    def validate_password(self):
        self.password_line_edit.setStyleSheet(
            f"QLineEdit {{ background-color: #0a7cee }}"
        )
        self.password_line_edit.setEnabled(False)
        time.sleep(0.5)
        global password
        password = self.password_line_edit.text()
        pass_hash = utils.hash_password(password)
        valid = pass_hash == utils.get_google_drive_password_hash()
        self.password_line_edit.valid = valid
        color = c.VALID_COLOR_MAP[valid]
        self.password_line_edit.setStyleSheet(
            f"QLineEdit {{ background-color: {color} }}"
        )
        time.sleep(0.5)
        self.password_line_edit.setEnabled(not valid)
        if valid:
            global screenmote
            screenmote = ScreenMote()
            navigate(self, screenmote)
        else:
            self.login_button.setEnabled(False)

    def validate_input(self):
        valid = len(self.password_line_edit.text().strip()) > 0
        color = c.VALID_COLOR_MAP[valid]
        self.password_line_edit.valid = valid
        self.password_line_edit.setStyleSheet(
            f"QLineEdit {{ background-color: {color} }}"
        )
        ready_check(self, self.validated_login_controls, self.login_inputs)


def navigate(self, next_):
    """
    navigate between two windows
    """
    global prev_
    prev_ = self
    position_next_window(prev_, next_)
    self.close()
    next_.show()


def position_next_window(prev_, next_):
    """
    Sets the position of the next_ window to the position of prev_ window
    whilst preserving the geometry of the next_ window
    """
    w = next_.geometry().width()
    h = next_.geometry().height()
    x = round(prev_.geometry().x() + prev_.geometry().width() / 2 - w / 2)
    y = round(prev_.geometry().y() + prev_.geometry().height() / 2 - h / 2)
    next_.setGeometry(x, y, w, h)


def center_window(self):
    frame_geometry = self.frameGeometry()
    screen = QtWidgets.QApplication.desktop().screenNumber(
        QtWidgets.QApplication.desktop().cursor().pos()
    )
    centerPoint = QtWidgets.QApplication.desktop().screenGeometry(screen).center()
    frame_geometry.moveCenter(centerPoint)
    self.move(frame_geometry.topLeft())


def ready_check(self, validated_controls, inputs):
    """
    Enables/disables a PyQt control when all vaidation checks return positive/negative
    """
    valid = all([input_.valid for input_ in inputs])
    for control in validated_controls:
        control.setEnabled(valid)


def communicate_update(args):
    ipv4, password, names, urls, display_times, delete = args
    ssh_client = utils.establish_connection(ipv4, password)
    command = construct_update_command(names, urls, display_times, delete)
    ext_status = utils.send_command(
        ssh_client, ipv4, password, command, sudo_required=False
    )
    return ext_status


def construct_update_command(names, urls, display_times, delete):
    args = " ".join(" ".join(tup) for tup in zip(names, urls, display_times))
    command = f"python3 /home/pi/deploy_assets.py {delete} {args}"
    return command


def scrape_display_times(urls, n_slides):
    display_times = []
    for i in range(len(urls)):
        sec_per_slide = round(float(urls[i].split("delayms=")[1]) / 1000.0)
        display_times.append(str(int(sec_per_slide * int(n_slides[i]))))
    return display_times


def update_assets(host_data, password, delete, names, urls, n_slides):

    host_data = [host for host in host_data if host["enabled"]]

    display_times = []
    for i in range(len(urls)):
        sec_per_slide = round(float(urls[i].split("delayms=")[1]) / 1000.0)
        display_times.append(str(int(sec_per_slide * int(n_slides[i]))))

    # urls need quotes for using as cmd line args
    urls = [f'"{url}"' for url in urls]

    host_data = utils.resolve_ipv4s(host_data)

    # screenly needs at least 2 assets because of memory leak issue
    if len(urls) == 1:
        names.append(names[0] + "_copy")
        urls.append(utils.augment_url(list(urls)[0]))
        display_times.append(display_times[0])

    exit_status = [
        communicate_update([host["ipv4"], password, names, urls, display_times, delete])
        for host in host_data
    ]
    output_status(exit_status)
    app.quit()


def power_cycle(host_data, command, password):

    host_data = [host for host in host_data if host["enabled"]]
    command = "sudo " + command + " now"
    host_data = utils.resolve_ipv4s(host_data)

    exit_status = [
        utils.toggle_power((host["ipv4"], password, command)) for host in host_data
    ]
    output_status(exit_status)
    app.quit()


def output_status(status):
    status = sorted(status, key=lambda x: "success" in x, reverse=True)
    print(*status, sep="\n", end="")


if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    if "Fusion" in QtWidgets.QStyleFactory.keys():
        app.setStyle("Fusion")

    login_portal = LoginPortal()
    login_portal.show()

    sys.exit(app.exec_())
