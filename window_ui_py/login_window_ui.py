# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './window_ui/login.ui'
#
# Created by: PyQt5 UI code generator 5.15.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_login_dialog(object):
    def setupUi(self, login_dialog):
        login_dialog.setObjectName("login_dialog")
        login_dialog.resize(364, 134)
        font = QtGui.QFont()
        font.setPointSize(12)
        login_dialog.setFont(font)
        self.verticalLayout = QtWidgets.QVBoxLayout(login_dialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.password_layout = QtWidgets.QFormLayout()
        self.password_layout.setObjectName("password_layout")
        self.verticalLayout.addLayout(self.password_layout)
        self.submit_login = QtWidgets.QPushButton(login_dialog)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.submit_login.setFont(font)
        self.submit_login.setObjectName("submit_login")
        self.verticalLayout.addWidget(self.submit_login)

        self.retranslateUi(login_dialog)
        QtCore.QMetaObject.connectSlotsByName(login_dialog)

    def retranslateUi(self, login_dialog):
        _translate = QtCore.QCoreApplication.translate
        login_dialog.setWindowTitle(_translate("login_dialog", "Login"))
        self.submit_login.setText(_translate("login_dialog", "Submit"))
