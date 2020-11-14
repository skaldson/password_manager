from PyQt5.QtCore import *
from PyQt5.QtWidgets import *


class InfoBox(QMessageBox):
    def __init__(self, my_parent, message):
        super(InfoBox, self).__init__()
        self.my_parent = my_parent
        self.message = message
        self.correct_input()

    def correct_input(self):
        message = QMessageBox.information(self.my_parent, 'Incorrect Input', self.message,
                                                        QMessageBox.Ok)

        if message == QMessageBox.Ok:
            return


class YesNoWindow(QMessageBox):
    def __init__(self, my_parent, message):
        super(YesNoWindow, self).__init__()
        self.my_parent = my_parent
        self.message = message

    def yes_no(self):
        message = QMessageBox.question(self.my_parent, 'Make Your Choose', self.message,
                                        QMessageBox.No|QMessageBox.Yes)

        if message == QMessageBox.Yes:
            return True
        elif message == QMessageBox.No:
            return False
