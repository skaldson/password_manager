from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *


class PasswordEdit(QLineEdit):
   
    def __init__(self, parent):
        self.parent = parent
        super().__init__(self.parent)

        self.setMaxLength(16)

        self.visibleIcon = QIcon("./images/visible_eye.png")
        self.hiddenIcon = QIcon("./images/invisible_eye.png")

        self.setEchoMode(QLineEdit.Password)
        self.togglepasswordAction = self.addAction(self.visibleIcon, QLineEdit.TrailingPosition)
        self.togglepasswordAction.triggered.connect(self.on_toggle_password_Action)
        self.password_shown = False


    def set_style(self):
        self.setStyleSheet("QLineEdit {\n"
                                    "font: 12pt \"Fira Sans Semi-Light\";\n"
                                    "}")
        self.setMaxLength(16)

    def on_toggle_password_Action(self):
        if not self.password_shown:
            self.setEchoMode(QLineEdit.Normal)
            self.password_shown = True
            self.togglepasswordAction.setIcon(self.hiddenIcon)
        else:
            self.setEchoMode(QLineEdit.Password)
            self.password_shown = False
            self.togglepasswordAction.setIcon(self.visibleIcon)
