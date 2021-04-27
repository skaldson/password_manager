import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

import db_files.init_db as init_db
# from db_files.db_cursor import DBCursor
from main_window import MainWindow
from greeting_window import WelcomeWindow
from user_info import UserInfo

class Uroboros:
    def __init__(self):
        self.init_members()


    def init_members(self):
        self.welcome_window = WelcomeWindow()
        self.main_window = MainWindow()
        self.welcome_part()

    def welcome_part(self):
        self.welcome_window.show()
        self.welcome_window.accepted.connect(self.show_main_window)
        self.welcome_window.get_user_id_signal.connect(self.init_user)


    def show_main_window(self):
        self.main_window.show()
        self.main_window.switch_user_signal.connect(self.restart_app)
        shortcut_close = QShortcut(QKeySequence('Ctrl+Q'), self.main_window)
        shortcut_close.activated.connect(lambda : self.main_window.close())

    def init_user(self, user_id, user_name, user_key):
        self.main_window.init_user_info(user_id, user_name, user_key)

    def restart_app(self):
        self.main_window.close()
        self.init_members()

    
if __name__ == "__main__":
    app = QApplication([])
    init_db.init_db()
    uroboros = Uroboros()
    sys.exit(app.exec_())
