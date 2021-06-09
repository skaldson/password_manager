from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import QtWidgets, uic

import window_ui_py.new_record_ui as new_record
from db_files.db_cursor import DBCursor
from widgets.password_edit import PasswordGenerate
from widgets.tags_widget import TagWidget
from windows.utility.message_boxes import InfoBox
from windows.records.tag_window import TagWindow
from windows.utility.abs_records import RecordAbsClass
from windows.user_info import UserInfo
from windows.correct_input import delete_rspace


class NewRecord(QDialog, new_record.Ui_new_record_dialog):

    record_init_signal = pyqtSignal(str, bytes, bytes, bytes, list)

    def __init__(self):
        super(NewRecord, self).__init__()
        self.setupUi(self)
        
        self.db_cursor = DBCursor.getInstance()
        self.init_objects()

    def init_objects(self):
        self.new_password = PasswordGenerate(self)
        self.new_password.set_style()

        self.label_password = QLabel('Password')
        self.new_login_layout.setGeometry(QRect(0, 0, 100, 200))
        self.label_password.setFont(QFont('Fira Sans Semi-Light', 12))
        self.new_login_layout.addRow(self.label_password, self.new_password)

        self.scroll_area.setWidget(self.tag_widget)


    def init_recording(self):
        self.setModal(True)
        self.submit_record.clicked.connect(self.add_new_record)
        self.show()        

    def add_new_record(self):
        login_name = delete_rspace(self.new_name.text())
        login = delete_rspace(self.new_login.text())
        password = self.new_password.text()
        tags = self.tag_widget.pressed_tags

        abstract_record = RecordAbsClass(self, login_name, login, password, tags)
        result_dict = abstract_record.result_forms_dict()
        
        if result_dict:
            result_login, result_password = result_dict['login'], result_dict['password']
            urandom = result_dict['urandom']
            self.record_init_signal.emit(login_name, result_login, result_password, urandom, tags)
            self.close()
