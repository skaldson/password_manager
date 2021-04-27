import sys
import os
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import QtWidgets

import cypher_func
import window_ui_py.main_window_ui as main_window
from binary_manipulators import set_user_photo
from db_files.db_cursor import DBCursor
from new_record import NewRecord
from message_boxes import InfoBox, YesNoWindow
from login import LoginWindowSerialize
from password_edit import PasswordEdit
from edit_section import EditSection
from custom_listwidget import CustomListWidget
from user_info import UserInfo


class MainWindow(QMainWindow, main_window.Ui_main_window):

    signal_init_edit_section = pyqtSignal(str, str, str)
    switch_user_signal = pyqtSignal()

    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)

        self.db_cursor = DBCursor.getInstance()

        self.init_functionality()
        
        
    def init_functionality(self):
        self.menu_new.triggered[QAction].connect(self.processtrigger_bar)

        self.stackedWidget.setCurrentIndex(1)

        self.user_info_button.clicked.connect(self.init_user_window)

        self.edit_section.hide_tool_button.clicked.connect(self.close_editing)
        self.edit_section.submit_signal.connect(self.edit_record_info)
        self.edit_section.tag_widget.signal_edit_tag.connect(self.edit_app_tag)
        self.edit_section.tag_widget.signal_add_tag.connect(self.add_new_tag)
        self.edit_section.tag_widget.signal_delete_tag.connect(self.delete_app_tag)
        self.adjustSize()


    def init_user_window(self):
        self.login_serializer = LoginWindowSerialize()
        self.login_serializer.window_mode = 2
        self.login_window = self.login_serializer.make_serialization()
        self.login_window.exit_user_signal.connect(self.switch_user)
        self.login_window.setModal(True)
        self.login_window.edit_user_signal.connect(self.update_user_info)
        self.login_window.show()

    def update_user_info(self, user_name, user_key):
        self.login_window.close()
        
        self.init_user_info(self.user_id, user_name, user_key)

    def switch_user(self):
        self.switch_user_signal.emit()

    # process menuBar actions
    def processtrigger_bar(self, trigger):
        if trigger == self.action_new_password:
            self.create_new_record_window()
        if trigger == self.action_delete_user:
            warning_message = "Are you really want delete all data?"
            window_title = "Delete Account"
            if YesNoWindow(self, title=window_title, message=warning_message).yes_no():
                self.db_cursor.delete_user()
                self.switch_user_signal.emit()
                # ця хуйня впала тут
            else:
                pass


    def close_editing(self):
        self.stackedWidget.setCurrentIndex(1)

    # init window for creating new login
    def create_new_record_window(self):
        self.new_record_window = NewRecord()
        self.new_record_window.record_init_signal.connect(self.new_user_record)

        self.new_record_window.tag_widget.signal_edit_tag.connect(self.edit_app_tag)
        self.new_record_window.tag_widget.signal_add_tag.connect(self.add_new_tag)
        self.new_record_window.tag_widget.signal_delete_tag.connect(self.delete_app_tag)
        
        self.new_record_window.init_recording()

    # init main key for program
    def init_user_info(self, current_id, user_name, user_key):
        self.user_info = UserInfo.getInstance()
        self.user_info.user_id = current_id
        self.user_id = self.user_info.user_id
        self.user_info.user_key = user_key
        self.user_info.user_name = user_name
        self.update_logins_list()
        self.user_info.user_photo = self.db_cursor.get_user_photo_by_id()
        set_user_photo(self.user_info.user_photo, self.user_info_button)

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
        init_info = self.db_cursor.get_full_user_info()
        self.logins_dict = {}
        for i in init_info:
            urandom = i[3]
            login_name = i[0]
            main_key = self.user_info.user_key
            login_decrypt = cypher_func.text_decryptor(main_key, i[1], urandom)
            password_decrypt = cypher_func.text_decryptor(main_key, i[2], urandom)
            # try:
            login_decrypt = login_decrypt.decode()
            password_decrypt = password_decrypt.decode()
            # except UnicodeDecodeError:
                # pass
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

            myQListWidgetItem = QListWidgetItem(self.logins_list)
            myQListWidgetItem.setSizeHint(temp.sizeHint())
            self.logins_list.addItem(myQListWidgetItem)
            self.logins_list.setItemWidget(myQListWidgetItem, temp)

    def record_delete_signal(self, login_name):
        login_id = (self.db_cursor.get_login_id(login_name))[0][0]
        self.db_cursor.delete_user_record(login_id)

        self.update_logins_list()
        self.close_editing()

    def set_item_info(self, login_name):
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
        self.update_logins_list()
