import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import QtWidgets, uic

import cypher_func
import window_ui_py.new_record_ui as new_record
from db_files.db_cursor import DBCursor
from password_edit import PasswordEdit
from tags_widget import TagWidget
from message_boxes import InfoBox
from tags_window import TagWindow


class NewRecord(QDialog, new_record.Ui_new_record_dialog):

    record_init_signal = pyqtSignal(str, bytes, bytes, bytes, list)

    def __init__(self):
        super(NewRecord, self).__init__()
        self.setupUi(self)
        
        self.db_cursor = DBCursor.getInstance()
        self.init_objects()

    def init_objects(self):
        self.new_password = PasswordEdit(self)
        self.new_password.set_style()

        self.label_password = QLabel('Password')
        self.new_login_layout.setGeometry(QRect(0, 0, 100, 200))
        self.label_password.setFont(QFont('Fira Sans Semi-Light', 12))
        self.new_login_layout.addRow(self.label_password, self.new_password)

        self.scroll_area.setWidget(self.tag_widget)


    def init_main_key(self, key):
        self.main_key = key

    def init_recording(self):
        self.setModal(True)
        self.submit_record.clicked.connect(self.add_new_record)
        self.show()        

    @property
    def user_records(self):
        temp_list = self.db_cursor.get_name_login
        names_login = []
        for i in temp_list:
            names_login.append(i[0])

        return names_login

    def add_new_record(self):
        names_login_list = self.user_records
        login_name, login, password = self.new_name.text(), self.new_login.text(), self.new_password.text()
        tags = self.tag_widget.pressed_tags

        condition = True
        if login and password and login_name:
            if login_name in names_login_list:
                condition = False
                InfoBox(self, 'Such login already exist')
            if len(password) < 8:
                condition = False
                InfoBox(self, 'Password must be at least 8 characters long')
            if len(tags) > 3:
                condition = False
                InfoBox(self, 'No more than 3 tags')

            if condition:
                encrypted_password, urandom = cypher_func.text_encryptor(self.main_key, password)
                encrypted_login = cypher_func.text_encryptor(self.main_key, login, urandom, False)

                self.record_init_signal.emit(login_name, encrypted_login, encrypted_password, urandom, tags)
                self.close()
