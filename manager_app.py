import sys

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

import db_files.init_db as init_db
from windows.generals.main_window import MainWindow
from windows.generals.start_window import WelcomeWindow
from import_export.remote.drive_connect import DriveConnect


class Uroboros:
    welcome_window = None
    main_window = None
    def __init__(self):
        self.init_members()

    def init_members(self):
        self.welcome_window = WelcomeWindow()
        self.welcome_window.setAttribute(Qt.WA_DeleteOnClose, True)
        self.main_window = MainWindow()
        self.main_window.setAttribute(Qt.WA_DeleteOnClose, True)
        self.welcome_part()

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

    def init_user(self, user_id, user_name, user_key):
        self.main_window.init_user_info(user_id, user_name, user_key)

    def restart_app(self):
        self.main_window.close()
        # self.main_window.disconnect()
        self.init_members()
        DriveConnect.remove_token()



if __name__ == "__main__":
    app = QApplication([])
    app.setStyle('Gtk2')
    init_db.init_db()
    uroboros = Uroboros()
    destroy_app = app.exec_()
    DriveConnect.remove_token()
    sys.exit(destroy_app)
