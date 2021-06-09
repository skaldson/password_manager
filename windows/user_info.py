import os

from files.binary_manage import binary_to_file
# from db_files.db_cursor import DBCursor


class UserInfo:
    __instance = None
    @staticmethod
    def getInstance():
        if UserInfo.__instance == None:
            UserInfo()
        return UserInfo.__instance
    def __init__(self):
        if UserInfo.__instance != None:
            raise Exception("This class is a UserInfo!")
        else:
            UserInfo.__instance = self
            self.init_class_members()


    def init_class_members(self):
        # self.db_cursor = DBCursor()
        self.__user_id = int()
        self.__user_key = bytes()
        self.__user_photo = bytes()
        self.__user_name = str()

    @property
    def user_id(self):
        return self.__user_id

    @user_id.setter
    def user_id(self, value):
        self.__user_id = value

    @property
    def user_name(self):
        return self.__user_name

    @user_name.setter
    def user_name(self, value):
        self.__user_name = value

    @property
    def user_key(self):
        return self.__user_key

    @user_key.setter
    def user_key(self, value):
        self.__user_key = value

    @property
    def user_photo(self):
        return self.__user_photo
    
    @user_photo.setter
    def user_photo(self, value):
        self.__user_photo = value

    def __str__(self):
        return f"user_id: {self.user_id}, user_key: {self.user_key} user_name:{self.user_name}"
