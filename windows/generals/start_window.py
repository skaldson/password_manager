import sys

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import QtWidgets, uic

import window_ui_py.greeting_window_py as welcome_window
from login_windows.serialize import LoginSerialize
from db_files.db_cursor import DBCursor


class WelcomeWindow(QDialog, welcome_window.Ui_greeting_window):
    get_user_id_signal = pyqtSignal(int, str, str)

    def __init__(self):
        super(WelcomeWindow, self).__init__()
        self.setupUi(self)
        self.db_cursor = DBCursor.getInstance()

        self.sign_in_button.clicked.connect(self.sign_in_window)
        self.sign_up_button.clicked.connect(self.sing_up_window)


    def accept_welcome(self):
        self.get_user_id_signal.emit(self.db_cursor.get_user_id_by_name(self.login_window.name), self.login_window.name, self.login_window.login_password.text())
        self.login_window.destroy()
        self.accept()

    # True - login mode, False - sign up mode
    def sign_in_window(self):
        self.create_login_window(True)

    def sing_up_window(self):
        self.create_login_window(mode=False)

    
    def create_login_window(self, mode):
        self.login_serializer = LoginSerialize()
        self.login_serializer.window_mode = mode
        self.login_window = self.login_serializer.make_serialization()
        self.login_window.setModal(True)
        self.login_window.show()
        self.login_window.accepted.connect(self.accept_welcome)
