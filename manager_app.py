import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

import db_files.init_db as init_db
from db_files.db_cursor import DBCursor
from login import LoginWindow
from main_window import MainWindow


def show_main_window():
    main_window.show()
    shortcut_close = QShortcut(QKeySequence('Ctrl+Q'), main_window)
    shortcut_close.activated.connect(lambda : main_window.close())
    main_window.init_main_key(login_window.get_main_key)

    
if __name__ == "__main__":
    app = QApplication([])
    init_db.init_db()
    login_window = LoginWindow()
    main_window = MainWindow()
    login_window.show()
    login_window.accepted.connect(show_main_window)
    sys.exit(app.exec_())
