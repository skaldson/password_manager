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
from custom_listwidget import CustomListWidget


class MainWindow(QMainWindow, main_window.Ui_main_window):

    signal_init_edit_section = pyqtSignal(str, str, str)

    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)

        self.db_cursor = DBCursor.getInstance()
        
        self.init_functionality()
        
        
    def init_functionality(self):
        self.menu_new.triggered[QAction].connect(self.processtrigger_bar)

        self.stackedWidget.setCurrentIndex(1)

        self.edit_section.hide_tool_button.clicked.connect(self.close_editing)
        self.edit_section.submit_signal.connect(self.edit_record_info)
        self.edit_section.tag_widget.signal_edit_tag.connect(self.edit_app_tag)
        self.edit_section.tag_widget.signal_add_tag.connect(self.add_new_tag)
        self.edit_section.tag_widget.signal_delete_tag.connect(self.delete_app_tag)

    # process menuBar actions
    def processtrigger_bar(self, trigger):
        if trigger == self.action_new_password:
            self.create_new_record_window()

    def close_editing(self):
        self.stackedWidget.setCurrentIndex(1)

    # init window for creating new login
    def create_new_record_window(self):
        self.new_record_window = NewRecord()
        self.new_record_window.record_init_signal.connect(self.new_user_record)

        self.new_record_window.tag_widget.signal_edit_tag.connect(self.edit_app_tag)
        self.new_record_window.tag_widget.signal_add_tag.connect(self.add_new_tag)
        self.new_record_window.tag_widget.signal_delete_tag.connect(self.delete_app_tag)
        

        self.new_record_window.init_main_key(self.main_key)
        self.new_record_window.init_recording()

    # init main key for program
    def init_main_key(self, key):
        self.main_key = key
        self.add_info_list_items()

    # record window edit signal
    def edit_app_tag(self, old_name, new_name, tag_colour):
        self.db_cursor.edit_tag(old_name, new_name, tag_colour)

    def add_new_tag(self, tag_name, tag_colour):
        self.db_cursor.add_new_tag(tag_name, tag_colour)

    def delete_app_tag(self, tag_index):
        self.db_cursor.delete_tag(tag_index)

    def new_user_record(self,login_name, login, password, urandom, tags):
        self.db_cursor.add_record_login(login_name, login, password, urandom)
        self.db_cursor.add_record_tag(login_name, tags)
        self.update_logins_list()


    def update_logins_list(self):
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

        # create custom widget with qmenu item, than add this widgets to our QListWidget
        for i in sorted(self.logins_dict.keys()):
            temp = CustomListWidget()
            temp.widget_label.setText(i)
            temp.widget_label.setStyleSheet("QLabel {\n"
                                    "font: 13pt \"Fira Sans Semi-Light\";\n"
                                    "}")
            temp.signal_delete_item.connect(self.record_delete_signal)
            temp.signal_press_item.connect(self.show_edit_section)
            temp.signal_init_main_key.connect(self.main_key_in_edit_section)
            

            myQListWidgetItem = QListWidgetItem(self.logins_list)
            myQListWidgetItem.setSizeHint(temp.sizeHint())
            self.logins_list.addItem(myQListWidgetItem)
            self.logins_list.setItemWidget(myQListWidgetItem, temp)

    def main_key_in_edit_section(self):
        self.edit_section.main_key = self.main_key

    def record_delete_signal(self, login_name):
        login_id = (self.db_cursor.get_login_id(login_name))[0][0]
        self.db_cursor.delete_login(login_id)

        self.update_logins_list()
        self.close_editing()


    def set_item_info(self, login_name):
        # self.current_login_name = login_name
        current_item_info = self.logins_dict[login_name]

        self.edit_section.login_name.setText(login_name)
        self.edit_section.login.setText(current_item_info['login'])

        self.edit_section.password.setText(current_item_info['passwd'])
        self.edit_section.init_record_name(login_name)
        self.edit_section.init_tags()
        self.edit_section.premordial_list = self.edit_section.get_forms_values()

    def show_edit_section(self, login_name):
        self.stackedWidget.setCurrentIndex(0)
        self.set_item_info(login_name)

    def edit_record_info(self, old_name, login_name, login, password, urandom, tags):
        self.db_cursor.update_intermediate(old_name, tags)

        self.db_cursor.edit_login(login_name, login, password, urandom, old_name)
        del self.logins_dict[old_name]
        self.logins_list.clear()
        self.add_info_list_items()

