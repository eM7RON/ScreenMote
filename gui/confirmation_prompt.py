# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'confirmation_prompt.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_ConfirmationPrompt(object):
    def setupUi(self, ConfirmationPrompt):
        ConfirmationPrompt.setObjectName("ConfirmationPrompt")
        ConfirmationPrompt.resize(260, 94)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            ConfirmationPrompt.sizePolicy().hasHeightForWidth()
        )
        ConfirmationPrompt.setSizePolicy(sizePolicy)
        ConfirmationPrompt.setMinimumSize(QtCore.QSize(260, 94))
        ConfirmationPrompt.setMaximumSize(QtCore.QSize(260, 94))
        ConfirmationPrompt.setSizeIncrement(QtCore.QSize(336, 0))
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(ConfirmationPrompt)
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
            20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding
        )
        self.verticalLayout_2.addItem(spacerItem)
        self.horizontalLayout_75 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_75.setObjectName("horizontalLayout_75")
        self.message = QtWidgets.QLabel(ConfirmationPrompt)
        self.message.setMinimumSize(QtCore.QSize(0, 25))
        self.message.setMaximumSize(QtCore.QSize(16777215, 25))
        self.message.setAlignment(QtCore.Qt.AlignCenter)
        self.message.setObjectName("message")
        self.horizontalLayout_75.addWidget(self.message)
        self.verticalLayout_2.addLayout(self.horizontalLayout_75)
        spacerItem1 = QtWidgets.QSpacerItem(
            20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding
        )
        self.verticalLayout_2.addItem(spacerItem1)
        self.horizontalLayout_76 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_76.setObjectName("horizontalLayout_76")
        self.yes_button = QtWidgets.QPushButton(ConfirmationPrompt)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.yes_button.sizePolicy().hasHeightForWidth())
        self.yes_button.setSizePolicy(sizePolicy)
        self.yes_button.setMinimumSize(QtCore.QSize(80, 25))
        self.yes_button.setMaximumSize(QtCore.QSize(80, 25))
        self.yes_button.setObjectName("yes_button")
        self.horizontalLayout_76.addWidget(self.yes_button)
        spacerItem2 = QtWidgets.QSpacerItem(
            20, 20, QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Minimum
        )
        self.horizontalLayout_76.addItem(spacerItem2)
        self.no_button = QtWidgets.QPushButton(ConfirmationPrompt)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.no_button.sizePolicy().hasHeightForWidth())
        self.no_button.setSizePolicy(sizePolicy)
        self.no_button.setMinimumSize(QtCore.QSize(80, 25))
        self.no_button.setMaximumSize(QtCore.QSize(80, 25))
        self.no_button.setObjectName("no_button")
        self.horizontalLayout_76.addWidget(self.no_button)
        self.verticalLayout_2.addLayout(self.horizontalLayout_76)
        self.horizontalLayout.addLayout(self.verticalLayout_2)
        self.horizontalLayout_2.addLayout(self.horizontalLayout)

        self.retranslateUi(ConfirmationPrompt)
        QtCore.QMetaObject.connectSlotsByName(ConfirmationPrompt)

    def retranslateUi(self, ConfirmationPrompt):
        _translate = QtCore.QCoreApplication.translate
        ConfirmationPrompt.setWindowTitle(
            _translate("ConfirmationPrompt", "ScreenMote")
        )
        self.message.setText(_translate("ConfirmationPrompt", "Are you Sure?"))
        self.yes_button.setToolTip(
            _translate("ConfirmationPrompt", "Confirm the action")
        )
        self.yes_button.setText(_translate("ConfirmationPrompt", "Yes"))
        self.no_button.setToolTip(
            _translate("ConfirmationPrompt", "Return to previous screen")
        )
        self.no_button.setText(_translate("ConfirmationPrompt", "No"))


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    ConfirmationPrompt = QtWidgets.QWidget()
    ui = Ui_ConfirmationPrompt()
    ui.setupUi(ConfirmationPrompt)
    ConfirmationPrompt.show()
    sys.exit(app.exec_())
