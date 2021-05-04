from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

import cypher_func
from db_files.db_cursor import DBCursor
from user_info import UserInfo
from message_boxes import InfoBox


def user_records():
        db_cursor = DBCursor.getInstance()
        temp_list = db_cursor.get_name_login()
        names_login = []
        for i in temp_list:
            names_login.append(i[0])

        return names_login

def is_unique_name(name_list, name, main_window):
    if name in name_list:
        print(name, name_list)
        InfoBox(main_window, 'Such login already exist')
        return False
    else:
        return True

class RecordAbsClass():
    def __init__(self, main_window, login_name, login, password, tags):
        self.main_window = main_window
        self.login_name = login_name
        self.login = login
        self.password = password
        self.tags = tags
        self.user_info = UserInfo.getInstance()

    def is_correct_forms(self, edit_section):
        names_login_list = user_records()
        login_name, login, password = self.login_name, self.login, self.password

        is_correct = True
        if login and password and login_name:
            if not edit_section:
                is_correct = is_unique_name(names_login_list, login_name, self.main_window)
            else:
                names_login_list.append(login_name)
                if names_login_list.count(login_name) > 1:
                    is_correct = True
                else:              
                    names_login_list.remove(login_name)
                    is_correct = is_unique_name(names_login_list, login_name, self.main_window)
            if len(password) < 8:
                is_correct = False
                InfoBox(self.main_window, 'Password must be at least 8 characters long')
            if len(self.tags) > 3:
                is_correct = False
                InfoBox(self.main_window, 'No more than 3 tags')
        else:
            InfoBox(self.main_window, 'Not all fields are completed')
            is_correct = False
        
        return is_correct

    def result_forms_dict(self, edit_section=False):
        result_dict = dict()
        encrypted_password, urandom, encrypted_login = str(), str(), str()
        if self.is_correct_forms(edit_section):
            encrypted_password, urandom = cypher_func.text_encryptor(self.user_info.user_key, self.password)
            encrypted_login = cypher_func.text_encryptor(self.user_info.user_key, self.login, urandom, False)
            result_dict = {'tags': self.tags, 'login_name':self.login_name, 'login': encrypted_login, 'password': encrypted_password, 'urandom': urandom}

        return result_dict
    