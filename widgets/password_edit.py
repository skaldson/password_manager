from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from crypto.ciphers import SecurePassword


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
                                    "font: 10pt \"Fira Sans Semi-Light\";\n"
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


class PasswordGenerate(PasswordEdit):
    def __init__(self, parent):
        self.parent = parent
        super().__init__(self.parent)

        self.generatePass = QIcon("./images/key.png")

        self.togglegenerateAction = self.addAction(self.generatePass, QLineEdit.TrailingPosition)
        self.togglegenerateAction.triggered.connect(self.on_toggle_generate_Action)

    def on_toggle_generate_Action(self):
        secure_password = SecurePassword()
        self.setText(secure_password.generate_secure_pass)
        self.password_shown = False
        self.on_toggle_password_Action()
