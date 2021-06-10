import os
import sqlite3

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import QtWidgets

import window_ui_py.login_window_ui as login_window
from db_files.db_cursor import DBCursor
from windows.user_info import UserInfo
from widgets.password_edit import PasswordEdit
from windows.utility.message_boxes import InfoBox
from files.binary_manage import convert_into_binary, binary_to_file
from files.binary_manage import set_user_photo, new_user_photo
from crypto.ciphers import generate_hash
from windows.correct_input import delete_rspace


class LoginSerialize(QDialog, login_window.Ui_login_dialog):
    def __init__(self):
        super(LoginSerialize, self).__init__()
        self.setupUi(self)
        self.db_cursor = DBCursor.getInstance()
        self.__window_mode = bool()

    @property
    def window_mode(self):
        return self.__window_mode

    @window_mode.setter
    def window_mode(self, value):
        self.__window_mode = value

    def make_serialization(self):
        if self.window_mode == 0:
            temp_window = Login()
            return temp_window
        elif self.window_mode == 1:
            temp_window = SignUp()
            return temp_window
        elif self.window_mode == 2:
            temp_window = EditUser()
            return temp_window

class Login(LoginSerialize):
    def __init__(self):
        super(Login, self).__init__()

    @property
    def init_edit_elements(self):
        self.login_password = PasswordEdit(self)
        self.login_password.set_style()
        self.password_layout.addRow(QLabel('Password'), self.login_password)
    
    @property
    def init_ui(self):
        self.photo_frame.hide()
        self.edit_user_button.setVisible(False)
        self.exit_user_button.setVisible(False)
        self.adjustSize()
        self.submit_login.clicked.connect(self.is_login)


    def is_login(self):
        self.name = self.user_name.text()
        self.key = self.login_password.text()
    
        if self.key and self.user_name:
            if self.db_cursor.that_user_exist(self.name):
                if self.db_cursor.is_correct_user_key(self.name, self.key):
                    self.accept()
                    return True
                else:
                    InfoBox(self, "Invalid Name or Password")
                    return False

class SignUp(LoginSerialize):
    def __init__(self):
        super(SignUp, self).__init__()
        self.user_info = UserInfo.getInstance()
        self.old_photo_path = ""
        
    @property
    def init_edit_fields(self):
        self.__user_photo = 0
        self.login_password = PasswordEdit(self)
        self.login_password.set_style()
        self.password_layout.addRow(QLabel('Password'), self.login_password)

        self.login_password_confirm = PasswordEdit(self)
        self.login_password_confirm.set_style()
        self.confirm_label = QLabel('Confirm Password')
        self.password_layout.addRow(self.confirm_label, self.login_password_confirm)


    @property
    def init_ui(self):
        self.setWindowTitle('Sign Up')
        self.edit_user_button.setVisible(False)
        self.exit_user_button.setVisible(False)
        self.user_photo_button.clicked.connect(self.init_user_photo)

        self.submit_login.clicked.connect(self.sign_up)

    @property
    def user_photo(self):
        return self.__user_photo

    @user_photo.setter
    def user_photo(self, value):
        self.__user_photo = value

    def setdefault_photo(self, value):
        if not value:
            set_user_photo(self.user_photo, self.user_photo_button, True)
        else:
            self.user_photo = value
            self.old_photo_path = self.user_photo[0].split('/')
            self.old_photo_path = self.old_photo_path[:-1]
            self.old_photo_path = '/'.join(self.old_photo_path)

    def check_photo_credentials(self):
        if self.old_photo_path:
            temp_value = new_user_photo(self, self.user_photo, self.user_photo_button, self.old_photo_path)
        else:
            temp_value = new_user_photo(self, self.user_photo, self.user_photo_button)
        self.setdefault_photo(temp_value)

    def init_user_photo(self):
        if self.user_photo:
            message = "What you want to do?"
            window_name = "Delete Photo"
            delete_item = InfoBox(my_parent=self, message=message, window_name=window_name, mode=False)
            if not delete_item.delete_status:
                self.user_photo_button.setIcon(QIcon())
                self.user_photo = 0
            elif delete_item.delete_status == 1:
                print(delete_item.delete_status)
                self.check_photo_credentials()
        else:
            self.check_photo_credentials()

    def sign_up(self):
        self.key = self.login_password.text()
        self.key_confirm = self.login_password_confirm.text()
        self.name = delete_rspace(self.user_name.text())
        try:
            user_photo = self.user_photo[0]
        except AttributeError:
            user_photo = False
        except TypeError:
            user_photo = self.user_photo
        

        if self.key and self.key_confirm and self.name:
            if not user_photo:
                user_photo = True
            if len(self.name) < 4:
                    InfoBox(self, 'Name must be at least 4 characters long')
                    return
            if self.key == self.key_confirm:
                if len(self.key) < 8:
                    InfoBox(self, 'Password must be at least 8 characters long')
                    return
                else:
                    try:
                        result_list = self.db_cursor.that_user_exist(self.name)
                        if result_list:
                            InfoBox(self, "User with such name already exist!")
                            return
                        else:
                            self.db_cursor.add_new_user(self.name, self.key, user_photo)
                            self.accept()
                    except sqlite3.IntegrityError:
                        pass
        else:
            InfoBox(self, "All fields must be filled")


class EditUser(SignUp):
    exit_user_signal = pyqtSignal()
    edit_user_signal = pyqtSignal(str, str)
    
    def __init__(self):
        super(EditUser, self).__init__()
        self.db_cursor = DBCursor.getInstance()
        self.user_info = UserInfo.getInstance()
        self.__edit_mode = False
        self.init_info_items()
        self.init_functionality()
        self.adjustSize()

    @property
    def init_ui(self):
        self.setWindowTitle('Edit User Info')
        self.submit_login.setVisible(False)
        self.confirm_label.setVisible(False)
        self.login_password_confirm.setVisible(False)

        # self.layout_bar = self.layout().setMenuBar(temp_bar)
        # self.menu_bar.show()
    
    def init_info_items(self):
        self.set_fields_text()
        self.read_only()
        self.user_photo = self.user_info.user_photo
        set_user_photo(self.user_photo, self.user_photo_button)

    def read_only(self, read=True):
        self.user_name.setReadOnly(read)
        self.login_password.setReadOnly(read)

    def set_fields_text(self):
        self.user_name.setText(self.user_info.user_name)
        self.login_password.setText(self.user_info.user_key)

    def init_functionality(self):
        self.edit_user_button.clicked.connect(self.set_edit_mode)
        self.exit_user_button.clicked.connect(self.switch_user)
        self.user_photo_button.clicked.connect(self.user_photo_window)
        self.submit_login.clicked.connect(self.change_user_info)

    def process_photo_button(self):
        signal = self.user_photo_button.clicked
        if self.edit_mode == False:
            old_slot = self.user_photo_window
            new_slot = self.init_user_photo
            self.reconnect_button(signal, new_slot=new_slot, old_slot=old_slot)
        elif self.edit_mode == True:
            old_slot = self.init_user_photo
            new_slot = self.user_photo_window
            self.reconnect_button(signal, new_slot=new_slot, old_slot=old_slot)
            
    
    def reconnect_button(self, signal, new_slot, old_slot):        
        try:
            signal.disconnect(old_slot)
            signal.connect(new_slot)
        except TypeError:
            pass

    @property
    def edit_mode(self):
        return self.__edit_mode
    
    @edit_mode.setter
    def edit_mode(self, value):
        self.__edit_mode = value

    def set_edit_mode(self):
        self.process_photo_button()
        if self.edit_mode == False:
            self.submit_login.setVisible(True)
            self.read_only(False)
            self.adjustSize()
        elif self.edit_mode == True:
            self.submit_login.setVisible(False)
            self.init_info_items()
            self.adjustSize()
        
        self.edit_mode = not self.edit_mode
        
    def switch_user(self):
        self.close()
        self.exit_user_signal.emit()
        
    def user_photo_window(self):
        photo_window = QDialog(self)
        label = QLabel(photo_window)
        file_name = './temp_image'
        self.user_photo_data = self.db_cursor.get_user_photo_by_id()
        if self.user_photo_data:
            binary_to_file(self.user_photo_data, file_name)
            image_pixmap = QPixmap(file_name)
            new_pixmap = image_pixmap.scaled(300, 300, Qt.KeepAspectRatio)
            window_width, window_height = new_pixmap.width(), new_pixmap.height()
            label.setPixmap(new_pixmap)
            photo_window.setFixedSize(QSize(window_width, window_height))
            os.remove(file_name)        
            photo_window.setModal(True)
            photo_window.show()
        else:
            pass

    def change_user_info(self):
        user_name = delete_rspace(self.user_name.text())
        user_key = self.login_password.text()
        identical_name = self.user_info.user_name == user_name
        identical_passwd = self.user_info.user_key == user_key
        identical_photo = self.user_info.user_photo == self.user_photo

        the_same_items = identical_name and identical_passwd and identical_photo

        if the_same_items:
            self.accept()
        else:
            if not identical_photo and not isinstance(self.user_photo, int):
                self.user_photo = convert_into_binary(self.user_photo[0])
            hash_name = generate_hash(self.user_name.text())
            hash_passwd = generate_hash(self.login_password.text())

            if self.db_cursor.that_user_exist(user_name) and user_name != self.user_info.user_name:
                InfoBox(self, 'User with such name already exist!', 'Info')
            else:
                self.db_cursor.update_user_info(hash_name, hash_passwd, self.user_photo)
                self.edit_user_signal.emit(user_name, user_key)
