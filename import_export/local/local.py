import ast
import os
import json

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

import crypto.ciphers as ciphers
from db_files.db_cursor import DBCursor
from windows.user_info import UserInfo
from windows.utility.message_boxes import InfoBox
from windows.utility.new_window_name import NewName


def init_logins_dict(tag_filter=False):
    db_cursor = DBCursor.getInstance()
    user_info = UserInfo.getInstance()
    if not tag_filter:
        init_info = db_cursor.get_full_user_info()
    else:
        init_info = db_cursor.get_full_user_info(tag_filter)
        for i in init_info:
            tags = i[-1]
            if tags == 0:
                del init_info[init_info.index(i)]
    logins_dict = {}

    for i in init_info:
        urandom = i[3]
        login_name = i[0]
        main_key = user_info.user_key
        login_decrypt = ciphers.text_decryptor(main_key, i[1], urandom)
        password_decrypt = ciphers.text_decryptor(main_key, i[2], urandom)
        login_decrypt = login_decrypt.decode()
        password_decrypt = password_decrypt.decode()
        colour = i[-2]
        tags = i[-1]

        temp_dict = {
                        'login': login_decrypt, 
                        'passwd': password_decrypt,
                        'colours':[colour], 
                        'tags': [tags]
                    }
        if login_name not in logins_dict:
            logins_dict.setdefault(login_name, temp_dict)
        else:
            (logins_dict[login_name]['colours']).append(colour)
            (logins_dict[login_name]['tags']).append(tags)

    return logins_dict

def generate_json():
    user_info = UserInfo.getInstance()
    logins_dict = init_logins_dict()

    global file_name
    file_name = user_info.user_name + '_records'
    with open(file_name, 'w') as login_str:
        json.dump(logins_dict, login_str, indent=4)
    return file_name

def enctypt_records():
    generate_json()
    user_info = UserInfo.getInstance()
    db_cursor = DBCursor.getInstance()
    user_urandom = db_cursor.get_user_urandom()

    key_str = user_info.user_name + "_" + user_info.user_key
    key_str = ciphers.generate_hash(key_str)

    file_obj = str()
    with open(file_name, 'r') as stream:
        file_obj = stream.read()

    encrypted_data = ciphers.text_encryptor(key_str, file_obj, user_urandom, False)

    with open(file_name, 'wb') as stream:
        stream.write(encrypted_data)

def decrypt_records(main_window):
    file_dialog = QFileDialog()
    user_folder = f"/home/{os.getlogin()}"
    db_cursor = DBCursor.getInstance()
    user_urandom = db_cursor.get_user_urandom()

    file_name = file_dialog.getOpenFileName(main_window, "Open File",
            user_folder, "Any Files (*)")
    
    if file_name[0]:
        user_info = UserInfo.getInstance()
        key_str = f"{user_info.user_name }_{user_info.user_key}"
        key_str = ciphers.generate_hash(key_str)
        try:
            with open(file_name[0], 'rb') as encrpt_str:
                encrypted_obj = encrpt_str.read()

            result = ciphers.text_decryptor(key_str, encrypted_obj, user_urandom)

            result = result.decode()

            result = dict(ast.literal_eval(result))
            return result
        except UnicodeDecodeError:
            message = "Invalid file"
            window_title = "Wrong file!"
            InfoBox(main_window, message, window_title)
            return False
