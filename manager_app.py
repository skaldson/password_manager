import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

import db_files.init_db as init_db
from main_window import MainWindow
from greeting_window import WelcomeWindow


class Uroboros:
    welcome_window = None
    main_window = None
    def __init__(self):
        self.init_members()

    def init_members(self):
        if self.welcome_window is None and self.main_window is None:
            self.welcome_window = WelcomeWindow()
            self.welcome_window.setAttribute(Qt.WA_DeleteOnClose, True)
            self.main_window = MainWindow()
            self.main_window.setAttribute(Qt.WA_DeleteOnClose, True)
            self.welcome_part()
        else:
            pass

    def welcome_part(self):
        self.welcome_window.show()
        self.welcome_window.accepted.connect(self.show_main_window)
        self.welcome_window.get_user_id_signal.connect(self.init_user)

    def show_main_window(self):
        self.main_window.show()
        self.main_window.switch_user_signal.connect(self.restart_app)
        self.welcome_window.get_user_id_signal.disconnect()
        self.welcome_window.accepted.disconnect()
        self.welcome_window.close()
        shortcut_close = QShortcut(QKeySequence('Ctrl+Q'), self.main_window)
        shortcut_close.activated.connect(lambda: self.main_window.close())

    def init_user(self, user_id, user_name, user_key):
        self.main_window.init_user_info(user_id, user_name, user_key)

    def restart_app(self):
        self.main_window.close()
        
        self.main_window = None
        self.welcome_window = None
        self.init_members()


if __name__ == "__main__":
    app = QApplication([])
    init_db.init_db()
    uroboros = Uroboros()
    sys.exit(app.exec_())
