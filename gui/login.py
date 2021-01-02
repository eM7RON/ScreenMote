# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'login.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Login(object):
    def setupUi(self, Login):
        Login.setObjectName("Login")
        Login.resize(260, 94)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Login.sizePolicy().hasHeightForWidth())
        Login.setSizePolicy(sizePolicy)
        Login.setMinimumSize(QtCore.QSize(260, 94))
        Login.setMaximumSize(QtCore.QSize(260, 94))
        Login.setSizeIncrement(QtCore.QSize(336, 0))
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(Login)
        self.horizontalLayout_2.setSpacing(3)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setSpacing(4)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.verticalLayout_2.addLayout(self.horizontalLayout_3)
        spacerItem = QtWidgets.QSpacerItem(
            20, 2, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed
        )
        self.verticalLayout_2.addItem(spacerItem)
        self.horizontalLayout_77 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_77.setObjectName("horizontalLayout_77")
        self.password_label = QtWidgets.QLabel(Login)
        self.password_label.setMinimumSize(QtCore.QSize(60, 0))
        self.password_label.setMaximumSize(QtCore.QSize(60, 16777215))
        self.password_label.setObjectName("password_label")
        self.horizontalLayout_77.addWidget(self.password_label)
        self.password_line_edit = QtWidgets.QLineEdit(Login)
        self.password_line_edit.setEchoMode(QtWidgets.QLineEdit.Password)
        self.password_line_edit.setObjectName("password_line_edit")
        self.horizontalLayout_77.addWidget(self.password_line_edit)
        self.verticalLayout_2.addLayout(self.horizontalLayout_77)
        self.horizontalLayout_75 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_75.setObjectName("horizontalLayout_75")
        self.login_button = QtWidgets.QPushButton(Login)
        self.login_button.setObjectName("login_button")
        self.horizontalLayout_75.addWidget(self.login_button)
        self.verticalLayout_2.addLayout(self.horizontalLayout_75)
        spacerItem1 = QtWidgets.QSpacerItem(
            10, 2, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed
        )
        self.verticalLayout_2.addItem(spacerItem1)
        self.horizontalLayout_76 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_76.setObjectName("horizontalLayout_76")
        self.verticalLayout_2.addLayout(self.horizontalLayout_76)
        self.horizontalLayout.addLayout(self.verticalLayout_2)
        self.horizontalLayout_2.addLayout(self.horizontalLayout)

        self.retranslateUi(Login)
        QtCore.QMetaObject.connectSlotsByName(Login)

    def retranslateUi(self, Login):
        _translate = QtCore.QCoreApplication.translate
        Login.setWindowTitle(_translate("Login", "ScreenMote"))
        self.password_label.setText(_translate("Login", "Password"))
        self.login_button.setText(_translate("Login", "Login"))


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    Login = QtWidgets.QWidget()
    ui = Ui_Login()
    ui.setupUi(Login)
    Login.show()
    sys.exit(app.exec_())
