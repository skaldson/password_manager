from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

import cypher_func
from compare_records import CompareRecords
from import_export import enctypt_user_records, decrypt_user_records
from import_export import init_logins_dict
import window_ui_py.main_window_ui as main_window
from binary_manipulators import set_user_photo
from db_files.db_cursor import DBCursor
from new_record import NewRecord
from message_boxes import YesNoWindow, InfoBox
from login import LoginWindowSerialize
from custom_listwidget import CustomListWidget
from user_info import UserInfo
from tags_widget import TagWidget
from new_name_form import NewName


class MainWindow(QMainWindow, main_window.Ui_main_window):
    switch_user_signal = pyqtSignal()

    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)

        self.db_cursor = DBCursor.getInstance()

        self.init_functionality()

    def init_functionality(self):
        self.menu_new.triggered[QAction].connect(self.processtrigger_bar)

        self.close_editing()

        self.user_info_button.clicked.connect(self.init_user_window)
        tag_sgn = {
                    'edit': self.edit_app_tag,
                    'add': self.add_new_tag,
                    'del': self.delete_app_tag
                    }
        self.edit_section.hide_tool_button.clicked.connect(self.close_editing)
        self.edit_section.submit_signal.connect(self.edit_record_info)
        self.edit_section.tag_widget.signal_edit_tag.connect(tag_sgn['edit'])
        self.edit_section.tag_widget.signal_add_tag.connect(tag_sgn['add'])
        self.edit_section.tag_widget.signal_delete_tag.connect(tag_sgn['del'])

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
        

    def processtrigger_bar(self, trigger):
        if trigger == self.action_new_password:
            self.create_new_record_window()
        if trigger == self.action_delete_user:
            message = "Are you really want delete all data?"
            window_title = "Delete Account"
            if YesNoWindow(self, title=window_title, message=message).yes_no():
                # self.db_cursor.delete_user()
                self.close()
                self.switch_user()
            else:
                pass
        if trigger == self.action_pass_export:
            enctypt_user_records()
        if trigger == self.action_pass_import:
            self.imported_logins = decrypt_user_records(self)
            if self.imported_logins:
                self.compare_logins_dict()

    def compare_logins_dict(self):
        first = self.logins_dict
        second = self.imported_logins
        self.compare_window = CompareRecords(first, second)
        self.compare_window.replace_login_signal.connect(self.replace_login_value)
        self.compare_window.add_new_login_signal.connect(self.add_imported_login)
        self.compare_window.unconflict_record_signal.connect(self.unconflict_record)
        self.compare_window.start_comparison()

    def unconflict_record(self, name):
        init_data = self.imported_logins[name]
        tags = self.imported_logins[name]['tags']
        result_tuple = self.check_record_data(init_data)

        self.submit_new_record(name, result_tuple, tags)

    def add_imported_login(self, name, title):
        self.old_record_name = name
        self.new_name_window = NewName()
        self.new_name_window.new_name_signal.connect(self.init_new_record_name)
        self.new_name_window.setWindowTitle(title)
        self.new_name_window.init_functionality()

    def check_record_data(self, data_dict):
        login = data_dict['login']
        passwd = data_dict['passwd']
        tags = data_dict['tags']
        colours = data_dict['colours']
        TagWidget.check_tags(tags, colours)
        user_key = self.user_info.user_key
        enc_passwd, urandom = cypher_func.text_encryptor(user_key, passwd)
        enc_login = cypher_func.text_encryptor(user_key, login, urandom, False)

        return (enc_login, enc_passwd, urandom)
    
    def submit_new_record(self, name, result_tuple, tags):
        enc_login, enc_passwd = result_tuple[0], result_tuple[1]
        urandom = result_tuple[-1]
        self.new_user_record(name, enc_login, enc_passwd, urandom, tags)
        self.hide_update_editing()

    def init_new_record_name(self, name):
        tags = self.imported_logins[self.old_record_name]['tags']
        record_data = self.imported_logins[self.old_record_name]
        result_tuple = self.check_record_data(record_data)
        self.submit_new_record(name, result_tuple, tags)

    def replace_login_value(self, name):
        tags = self.imported_logins[name]['tags']
        result_tuple = self.check_record_data(self.imported_logins[name])
        enc_login, enc_passwd = result_tuple[0], result_tuple[1]
        urandom = result_tuple[-1]
        
        self.edit_record_info(name, name, enc_login, enc_passwd, urandom, tags)
        self.hide_update_editing()

    def hide_update_editing(self):
        self.update_logins_list()
        self.close_editing()

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

    def new_user_record(self, login_name, login, password, urandom, tags):
        self.db_cursor.add_record_login(login_name, login, password, urandom)
        self.db_cursor.add_record_tag(login_name, tags)
        self.update_logins_list()

    def update_logins_list(self):
        self.logins_list.clear()
        self.add_info_list_items()

    def init_logins_dict(self):
        self.logins_dict = init_logins_dict()

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

        self.hide_update_editing()

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
