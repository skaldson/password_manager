from PyQt5.QtCore import *
from PyQt5.QtWidgets import *


class InfoBox(QMessageBox):
    def __init__(self, my_parent, message, window_name='Incorrect Input', mode=True):
        super(InfoBox, self).__init__()
        self.my_parent = my_parent
        self.message = message
        self.window_name = window_name
        self.mode = mode
        self.serialize_window()
        

    def serialize_window(self):
        if self.mode == True:
            self.correct_input()
        elif self.mode == False:
            self.delete_item()
        self.adjustSize()


    def correct_input(self):
        message = QMessageBox.information(self.my_parent, self.window_name, self.message,
                                                        QMessageBox.Ok)

        if message == QMessageBox.Ok:
            return

    def delete_item(self):
        delete_box = QMessageBox(self.my_parent)
        delete_box.setText(self.message)
        delete_box.setWindowTitle(self.window_name)
        delete_box.addButton(QPushButton('Delete Photo'), QMessageBox.YesRole)
        delete_box.addButton(QPushButton('Change Photo'), QMessageBox.NoRole)
        self.delete_status = delete_box.exec_()
        

class YesNoWindow(QMessageBox):
    def __init__(self, my_parent, message, title='Make Your Choose'):
        super(YesNoWindow, self).__init__()
        self.my_parent = my_parent
        self.message = message
        self.title = title

    def yes_no(self):
        message = QMessageBox.question(self.my_parent, self.title, self.message,
                                        QMessageBox.No|QMessageBox.Yes)

        if message == QMessageBox.Yes:
            return True
        elif message == QMessageBox.No:
            return False
