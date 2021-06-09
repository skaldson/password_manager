# DBCursor class, singleton pattern
import sqlite3
import sys
import os

from crypto.ciphers import generate_hash, text_encryptor
from files.binary_manage import convert_into_binary
from windows.user_info import UserInfo

sys.path.append('.')


class DBCursor:
    __instance = None

    @staticmethod
    def getInstance():
        if DBCursor.__instance is None:
            DBCursor()
        return DBCursor.__instance

    def __init__(self):
        if DBCursor.__instance is not None:
            raise Exception("This class is a DBCursor!")
        else:
            DBCursor.__instance = self
            self.set_db_manipulators()

    def set_db_manipulators(self):
        self.__db_name = './db_files/Logins.db'
        self.db_connector = sqlite3.connect(self.__db_name)
        self.db_cursor = self.db_connector.cursor()
        self.user_info = UserInfo.getInstance()

    def init_new_user_tags(self):
        user_id = self.user_info.user_id
        query = """SELECT Tag FROM Tags WHERE User_ID='%s'""" % (user_id)
        self.db_cursor.execute(query)
        query_result = self.db_cursor.fetchall()

        if not query_result:
            query_insert = f"""INSERT INTO `Tags`(`Tag`, `Colour_ID`, `User_ID`) VALUES
                                ('facebook', 3, {user_id}),
                                ('twitter', 3, {user_id}),
                                ('reddit', 2, {user_id}),
                                ('personal', 6, {user_id}),
                                ('mail', 1, {user_id});"""

            self.db_cursor.execute(query_insert)
            self.db_connector.commit()
        else:
            pass

    def add_new_user(self, name, key, image):
        urandom = os.urandom(16)
        query = """INSERT INTO `Users`(`Name`, `Key`, `Image`, `Urandom`) VALUES
                        (?, ?, ?, ?)"""

        name = generate_hash(name)
        key = generate_hash(key)
        image = convert_into_binary(image)
        data_tuple = (name, key, image, urandom)

        self.db_cursor.execute(query, data_tuple,)
        self.db_connector.commit()

    def that_user_exist(self, user_name):
        query = """SELECT Name FROM `Users` WHERE `Name` IN (?)"""

        user_name = generate_hash(user_name)
        self.db_cursor.execute(query, (user_name,))

        return self.db_cursor.fetchall()

    def is_correct_user_key(self, user_name, user_key):
        query = """SELECT `Key` FROM `Users` WHERE `Name`=? AND `Key`=?"""

        user_name = generate_hash(user_name)
        user_key = generate_hash(user_key)
        self.db_cursor.execute(query, (user_name, user_key,))

        return self.db_cursor.fetchall()

    def get_user_id_by_name(self, user_name):
        query = """SELECT `ID` FROM `Users` WHERE `Name`=?"""

        user_name = generate_hash(user_name)
        self.db_cursor.execute(query, (user_name,))
        return (self.db_cursor.fetchall())[0][0]

    def get_user_key_by_id(self):
        query = """SELECT `Key` FROM `Users`
                    WHERE `ID`='%s'""" % (self.user_info.user_id,)

        self.db_cursor.execute(query)
        return (self.db_cursor.fetchall())[0][0]

    def get_user_urandom(self):
        user_id = self.user_info.user_id
        query = """SELECT Urandom FROM Users WHERE ID='%s'""" % (user_id)

        self.db_cursor.execute(query)
        return (self.db_cursor.fetchall())[0][0]

    # getters
    @property
    def get_tag_names(self):
        query = """SELECT Tag FROM Tags 
            WHERE User_ID='%s'""" % (self.user_info.user_id)

        self.db_cursor.execute(query)
        return self.db_cursor.fetchall()

    @property
    def get_tag_and_colour(self):
        query = """SELECT Tag, Colour.Colour FROM Tags, Colour
                    WHERE Tags.Colour_ID=Colour.ID
                        AND Tags.User_ID='%s'""" % (self.user_info.user_id)

        self.db_cursor.execute(query)
        return self.db_cursor.fetchall()

    def get_special_tag_and_colour(self, exceptions):
        user_id = self.user_info.user_id
        exceptions = str(exceptions)
        exceptions = exceptions.replace('[', '(')
        exceptions = exceptions.replace(']', ')')
        query = """SELECT Tag, Colour.Colour FROM Tags, Colour
                    WHERE Tags.Colour_ID=Colour.ID
                    AND Tags.User_ID='%s'
                    AND Tag NOT IN %s""" % (user_id, exceptions)

        self.db_cursor.execute(query)
        return self.db_cursor.fetchall()

    def get_name_login(self):
        query = """SELECT Logins.Login_Name FROM Logins
            WHERE Logins.User_ID='%s'""" % (self.user_info.user_id,)

        self.db_cursor.execute(query)
        return self.db_cursor.fetchall()

    def get_intermediate_tag_id(self, tag_name):
        data_tuple = (tag_name, self.user_info.user_id)
        query = """SELECT Intermediate.Tag_ID FROM Tags, Intermediate WHERE
                    Tags.Id=Intermediate.Tag_ID
                        AND Tags.Tag='%s' AND Tags.User_ID='%s'""" % data_tuple

        self.db_cursor.execute(query)
        return self.db_cursor.fetchall()

    def get_tags_by_login_name(self, login_name):
        user_id = self.user_info.user_id
        data_tuple = (login_name, user_id, user_id)
        query = """SELECT Tags.Tag, Colour.Colour FROM Tags, Colour
                    WHERE Tags.ID IN (SELECT Tag_ID FROM
                    Intermediate, Logins WHERE
                    Intermediate.Login_ID=Logins.ID AND
                    Logins.Login_Name='%s' AND 
                    Intermediate.User_ID='%s') AND
                    Tags.Colour_ID=Colour.ID AND
                    Tags.User_ID='%s'""" % data_tuple

        self.db_cursor.execute(query)
        return self.db_cursor.fetchall()

    def get_tag_id_by_name(self, tag_name):
        data_tuple = (tag_name, self.user_info.user_id,)
        query = """SELECT Tags.ID FROM Tags 
            WHERE Tags.Tag='%s' AND Tags.User_ID='%s'""" % data_tuple

        self.db_cursor.execute(query)
        return self.db_cursor.fetchall()[0][0]

    @property
    def get_colors(self):
        query = """SELECT Colour.Colour FROM Colour"""

        self.db_cursor.execute(query)
        return self.db_cursor.fetchall()

    def get_colour_by_id(self, colour_id):
        query = """SELECT Colour.Colour FROM Colour
                    WHERE Colour.ID='%s'""" % (colour_id)

        self.db_cursor.execute(query)
        return self.db_cursor.fetchall()

    def get_colour_by_name(self, colour_name):
        query = """SELECT Colour.ID FROM Colour
                    WHERE Colour.Colour='%s'""" % (colour_name)

        self.db_cursor.execute(query)
        return self.db_cursor.fetchall()

    def get_login_id(self, login_name):
        query = """SELECT Logins.ID FROM `Logins` INNER JOIN `Users`
                ON Logins.User_ID=Users.ID WHERE Logins.Login_Name=?
                    AND Users.ID=?"""
        data_tuple = (login_name, self.user_info.user_id,)

        self.db_cursor.execute(query, data_tuple)
        return self.db_cursor.fetchall()

    def get_full_user_info(self):
        user_id = self.user_info.user_id
        query_inter = """SELECT Logins.Login_Name, Logins.Login, Logins.Password,
                    Logins.Urandom, Colour.Colour as Colour, Tags.Tag
                    FROM Logins, Colour, Intermediate, Tags WHERE Intermediate.Tag_ID=Tags.ID AND
					Intermediate.Login_ID=Logins.ID AND Colour.ID IN (SELECT Colour.ID
					FROM Colour INNER JOIN Tags ON Colour.ID=Tags.Colour_ID WHERE
					Tags.ID=Intermediate.Tag_ID) AND Intermediate.User_ID='%s'""" % (user_id,)

        query_log = """SELECT Logins.Login_Name, Logins.Login, Logins.Password,
                    Logins.Urandom, 0 as Colour, 0 as Tags 
                    FROM Logins WHERE Logins.User_ID='%s' AND
					Logins.ID NOT IN (SELECT Login_ID FROM Intermediate)""" % (user_id)

        query = f"{query_inter} UNION {query_log}"
        
        self.db_cursor.execute(query)
        return self.db_cursor.fetchall()

    def get_login_id_by_name(self, login_name):
        user_id = self.user_info.user_id
        query = """SELECT Logins.ID FROM `Logins`, `Users`
            WHERE Logins.User_ID=Users.ID AND Logins.Login_Name='%s'
                AND Logins.User_ID='%s'""" % (login_name, user_id,)

        self.db_cursor.execute(query)
        return (self.db_cursor.fetchall())[0][0]

    def get_user_photo_by_id(self):
        query = """SELECT Image FROM Users
                    WHERE ID='%s'""" % (self.user_info.user_id,)

        self.db_cursor.execute(query)
        return (self.db_cursor.fetchall())[0][0]

    # manipulators
    def add_record_login(self, login_name, user_login, user_password, urandom):
        user_id = self.user_info.user_id
        query = """INSERT INTO Logins(Login_Name, Login,
                                        Password, Urandom, User_ID)
                                            VALUES(?, ?, ?, ?, ?)"""
        data_tuple = (login_name, user_login, user_password, urandom, user_id,)

        self.db_cursor.execute(query, data_tuple)
        self.db_connector.commit()

    def add_record_tag(self, login_name, tags):
        login_id = self.get_login_id_by_name(login_name)
        user_id = self.user_info.user_id
        try:
            if tags[0] == 0:
                pass
            else:
                for i in tags:
                    current_tag_id = (self.get_tag_id_by_name(i))
                    query = """INSERT INTO `Intermediate`
                            (Tag_ID, Login_ID, User_ID) VALUES(?, ?, ?);"""
                    data_tuple = (current_tag_id, login_id, user_id,)
                    self.db_cursor.execute(query, data_tuple)

                self.db_connector.commit()
        except IndexError:
            pass

    def add_new_tag(self, tag_name, tag_colour):
        data_tuple = (tag_name, tag_colour, self.user_info.user_id)
        query = """INSERT INTO `Tags` (`Tag`, `Colour_ID`, `User_ID`)
                        VALUES ('%s', '%s', '%s')""" % data_tuple

        self.db_cursor.execute(query)
        self.db_connector.commit()

    # edit tag
    def edit_tag(self, old_name, new_name, tag_colour):
        query = """UPDATE `Tags` SET Tag=?, Colour_ID=? 
                    WHERE Tag=? AND User_ID=?"""
        data_tuple = (new_name, tag_colour, old_name, self.user_info.user_id)

        self.db_cursor.execute(query, data_tuple)
        self.db_connector.commit()

    def delete_tag(self, tag_name):
        query = """DELETE FROM Tags WHERE Tag='%s' 
                    AND User_ID='%s'""" % (tag_name, self.user_info.user_id)

        self.db_cursor.execute(query)
        self.db_connector.commit()

    def unselect_tag(self, login_name, tag_name):
        tag_id = self.get_tag_id_by_name(tag_name)
        login_id = self.get_login_id_by_name(login_name)
        query = """DELETE FROM `Intermediate` WHERE Tag_ID=? 
                    AND Login_ID=? AND User_ID=?"""
        data_tuple = (tag_id, login_id, self.user_info.user_id,)

        self.db_cursor.execute(query, data_tuple)
        self.db_connector.commit()

    def delete_user_record(self, login_id):
        self.db_cursor.execute('BEGIN')
        try:
            user_id = self.user_info.user_id
            delete_intermediate = """DELETE FROM `Intermediate`
                WHERE Intermediate.Login_ID='%s' 
                    AND Intermediate.User_ID='%s'""" % (login_id, user_id)

            delete_record = """DELETE FROM `Logins` WHERE
                Logins.ID IN (SELECT Logins.ID FROM Logins INNER JOIN Users ON
                    Logins.User_ID=Users.ID WHERE Logins.ID='%s'
                        AND Users.ID='%s')""" % (login_id, user_id)

            self.db_cursor.execute(delete_intermediate)
            self.db_cursor.execute(delete_record)
        except sqlite3.Error:
            print('failed!')
            print('rollback!')

        self.db_connector.commit()

    def edit_login(self, login_name, login, password, urandom, old_name):
        query = """UPDATE Logins SET Login_Name=?, Login=?,
                        Password=?, Urandom=? WHERE `Login_Name`=?
                            AND `User_ID`=?"""
        user_id = self.user_info.user_id
        data_tuple = (login_name, login, password, urandom, old_name, user_id,)

        self.db_cursor.execute(query, data_tuple)
        self.db_connector.commit()

    def get_intermediate_rows_by_user_id(self, login_id):
        query = """SELECT Intermediate.Tag_ID, Intermediate.Login_ID
                    FROM Intermediate INNER JOIN Users
                        ON Intermediate.User_ID=Users.ID
                            WHERE Intermediate.Login_ID=?
                                AND Intermediate.User_ID=?"""
        data_tuple = (login_id, self.user_info.user_id,)

        self.db_cursor.execute(query, data_tuple)
        return self.db_cursor.fetchall()

    def delete_login_from_intermediate(self, name):
        login_id = self.get_login_id_by_name(name)
        data_tuple = (login_id, self.user_info.user_id)
        query = """DELETE FROM Intermediate WHERE
                    Login_ID='%s' AND User_ID='%s'""" % data_tuple

        self.db_cursor.execute(query)
        self.db_connector.commit()           

    def update_intermediate(self, login_name, tags):
        login_id = self.get_login_id_by_name(login_name)
        available_tags = self.get_intermediate_rows_by_user_id(login_id)

        for i in tags:
            if i == 0:
                break
            tag_id = self.get_tag_id_by_name(i)
            if available_tags:
                temp = (tag_id, login_id)
                if temp in available_tags:
                    continue
                else:
                    query = """INSERT INTO `Intermediate`
                        (Tag_ID, Login_ID, User_ID)
                            VALUES(?, ?, ?);"""
                    data_tuple = (tag_id, login_id, self.user_info.user_id,)
            else:
                if [tag_id, login_id] in available_tags:
                    continue
                else:
                    query = """INSERT INTO `Intermediate`
                                (Tag_ID, Login_ID, User_ID)
                                    VALUES(?, ?, ?);"""
                    data_tuple = (tag_id, login_id, self.user_info.user_id,)

            self.db_cursor.execute(query, data_tuple)

        self.db_connector.commit()

    def update_user_info(self, new_name, new_passwd, new_photo):
        query = """UPDATE `Users` SET Name=?, Key=?, Image=? WHERE ID=?"""
        data_tuple = (new_name, new_passwd, new_photo, self.user_info.user_id,)

        self.db_cursor.execute(query, data_tuple)
        self.db_connector.commit()

    def get_user_data(self):
        query = """SELECT Name, Key FROM Users
            WHERE ID='%s'""" % (self.user_info.user_id,)

        self.db_cursor.execute(query)
        return (self.db_cursor.fetchall())[0]

    # FUCK THIS SHIT
    def delete_user(self):
        query_intrmd_del = """DELETE FROM Intermediate WHERE User_ID=?"""
        query_logins_del = """DELETE FROM Logins WHERE User_ID=?"""
        query_tags_del = """DELETE FROM Tags WHERE User_ID=?"""
        query_user_del = """DELETE FROM Users WHERE ID=?"""
        data_tuple = (self.user_info.user_id,)

        self.db_cursor.execute('BEGIN')
        try:
            query_list = [query_intrmd_del, 
                            query_logins_del,
                            query_tags_del,
                            query_user_del]

            for query in query_list:
                self.db_cursor.execute(query, data_tuple)

        except sqlite3.Error:
            print('failed!\nrollback!')

        self.db_connector.commit()
