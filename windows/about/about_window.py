from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

import window_ui_py.about_py as about_window


class AboutWindow(QDialog, about_window.Ui_Dialog):
    def __init__(self):
        super(AboutWindow, self).__init__()
        self.setupUi(self)

    def init_functionality(self):
        self.setModal(True)
        self.exec_()
 