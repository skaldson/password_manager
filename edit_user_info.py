# import sys
# from PyQt5.QtWidgets import *
# from PyQt5.QtGui import *
# from PyQt5.QtCore import *
# from PyQt5 import QtWidgets

# from login import LoginWindowSerialize
# from cypher_func import generate_hash, convert_into_binary
# from db_files.db_cursor import DBCursor
# from user_info import UserInfo
# from main_window import MainWindow

# class EditUserInfo(LoginWindowSerialize):
#     exit_user_signal = pyqtSignal()
    
#     def __init__(self):
#         super(EditUserInfo, self).__init__()
#         self.db_cursor = DBCursor.getInstance()
#         self.user_info = UserInfo.getInstance()
#         self.__edit_mode = False
#         MainWindow.set_user_photo(self.user_photo_button)
#         self.user_name.setText(self.user_info.user_name)
#         print(self.user_info)
#         # self.user_id = int()


#     @property
#     def init_ui(self):
#         self.setWindowTitle('Edit User Info')
#         self.edit_user_button.clicked.connect(self.set_edit_mode)
#         self.exit_user_button.clicked.connect(self.switch_user)


#     def init_edit_elements(self):
#         self.login_password = PasswordEdit(self)
#         self.login_password.set_style()
#         self.password_layout.addRow(QLabel('Password'), self.login_password)
        


#     @property
#     def edit_mode(self):
#         return self.__edit_mode

#     def set_edit_mode(self):
#         self.__edit_mode = True

#     def switch_user(self):
#         self.exit_user_signal.emit()
        
        
