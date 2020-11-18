import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import QtWidgets

import cypher_func
import window_ui_py.main_window_ui as main_window
from db_files.db_cursor import DBCursor
from new_record import NewRecord
from message_boxes import InfoBox
from login import LoginWindow
from password_edit import PasswordEdit
from edit_section import EditSection


class MainWindow(QMainWindow, main_window.Ui_main_window):

    signal_init_edit_section = pyqtSignal(str, str, str)

    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)

        self.db_cursor = DBCursor.getInstance()
        self.edit_section.password = PasswordEdit(self.edit_section)
        self.pass_label = QLabel('Password')
        self.init_functionality()
        
        
    # init main window functionality
    def init_functionality(self):
        self.add_record_button.clicked.connect(self.create_new_record_window)
        self.edit_section.hide()
        self.logins_list.itemClicked.connect(self.init_edit_section)
        self.edit_section.cancel_editing.clicked.connect(self.set_item_info)
        self.edit_section.hide_tool_button.clicked.connect(self.edit_section.hide)

    # init window for creating new login
    def create_new_record_window(self):
        self.new_record_window = NewRecord()
        self.new_record_window.record_init_signal.connect(self.new_user_record)

        self.new_record_window.tag_widget.signal_edit_tag.connect(self.edit_app_tag)
        self.new_record_window.tag_widget.signal_add_tag.connect(self.add_new_app_tag)
        self.new_record_window.tag_widget.signal_delete_tag.connect(self.delete_app_tag)
        
        self.new_record_window.init_main_key(self.main_key)
        self.new_record_window.init_recording()

    # init main key for program
    def init_main_key(self, key):
        self.main_key = key
        self.add_info_list_items()

    # record window edit signal
    def edit_app_tag(self, tag_index, tag_name, tag_colour):
        self.db_cursor.edit_tag(tag_index, tag_name, tag_colour)

    def add_new_app_tag(self, tag_index, tag_name, tag_colour):
        self.db_cursor.add_new_tag(tag_index, tag_name, tag_colour)

    def delete_app_tag(self, tag_index):
        self.db_cursor.delete_tag(tag_index)

    def new_user_record(self,login_name, login, password, urandom, tags):
        self.db_cursor.add_record_tag(tags)
        self.db_cursor.add_record_login(login_name, login, password, urandom)
        self.logins_list.clear()
        self.add_info_list_items()

    def init_logins_dict(self):
        init_info = self.db_cursor.get_full_user_info
        self.logins_dict = {}
        for i in init_info:
            urandom = i[3]
            login_name = i[0]
            login_decrypt = (cypher_func.text_decryptor(self.main_key, i[1], urandom)).decode()
            password_decrypt = (cypher_func.text_decryptor(self.main_key, i[2], urandom)).decode()
            colour = i[-2]
            tags = i[-1]

            temp_dict = {'login': login_decrypt, 'passwd': password_decrypt, 'colours':[colour], 'tags': [tags]}
            if login_name not in self.logins_dict:
                self.logins_dict.setdefault(login_name, temp_dict)
            else:
                (self.logins_dict[login_name]['colours']).append(colour)
                (self.logins_dict[login_name]['tags']).append(tags)

    def add_info_list_items(self):
        self.init_logins_dict()
        # print(self.logins_dict)

        for i in sorted(self.logins_dict.keys()):
            temp = QListWidgetItem(i)
            self.logins_list.addItem(temp)

    def set_item_info(self):
        current_item = self.logins_list.currentItem()
        current_item_info = self.logins_dict[current_item.text()]

        self.edit_section.login_name.setText(current_item.text())
        self.edit_section.login.setText(current_item_info['login'])

        
        self.pass_label.setFont(QFont('Fira Sans Semi-Light', 12))
        self.edit_section.password.set_style()
        self.edit_section.password.setText(current_item_info['passwd'])
        self.edit_section.data_layout.addRow(self.pass_label, self.edit_section.password)

        # self.edit_section.password_edit.show()

    def init_edit_section(self):
        self.edit_section.show()
        self.edit_section.init_record_index(self.logins_list.currentItem().text())
        self.edit_section.init_edit_tag_list()
        # self.edit_section.edit_tag_widget.print_record_index()
        # print(self.edit_section.current_record_id)
        self.set_item_info()

    def submit_editing(self):
        pass
