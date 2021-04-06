import sys
import sqlite3
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import QtWidgets

import window_ui_py.login_window_ui as login_window
from db_files.db_cursor import DBCursor
from message_boxes import InfoBox
from password_edit import PasswordEdit
from cypher_func import generate_hash


class LoginWindow(QDialog, login_window.Ui_login_dialog):
    def __init__(self):
        super(LoginWindow, self).__init__()
        self.setupUi(self)
        self.db_cursor = DBCursor.getInstance()
        self.is_exist_key()


    def is_exist_key(self):
        if self.db_cursor.get_main_key:
            self.login_password_confirm.setVisible(False)
            self.password_confirm_label.setVisible(False)
            self.submit_login.clicked.connect(self.is_login)
        else:
            self.setWindowTitle('Sign Up')
            self.submit_login.clicked.connect(self.sign_up)

    @property
    def init_edit_fields(self):
        self.login_password = PasswordEdit(self)
        self.login_password.set_style()
        self.login_password.setText('12345678')
        self.password_layout.addRow(QLabel('Password'), self.login_password)
        self.login_password_confirm = PasswordEdit(self)
        self.login_password_confirm.set_style()
        self.password_confirm_label = QLabel('Confirm Password')
        self.password_layout.addRow(self.password_confirm_label, self.login_password_confirm)

    def is_login(self):
        self.key = self.login_password.text()

        if self.key:
            if (self.db_cursor.get_main_key)[0][0] == generate_hash(self.key):
                self.accept()
                return True
            else:
                return False

    @property
    def get_main_key(self):
        return self.key

    def sign_up(self):
        self.key = self.login_password.text()
        self.key_confirm = self.login_password_confirm.text()

        if self.key and self.key_confirm:
            if len(self.key) < 8:
                InfoBox(self, 'Password must be at least 8 characters long')
            else:
                if self.key != self.key_confirm:
                    self.login_password_confirm.setStyleSheet('border: 1px solid red;')
                else:
                    self.login_password_confirm.setStyleSheet('border: 0px;')
                    try:
                        self.accept()
                        self.db_cursor.init_main_key(generate_hash(self.key))
                    except sqlite3.IntegrityError:
                        pass
        elif (self.key and (not self.key_confirm)):
            self.login_password_confirm.setStyleSheet('border-color: red;')
