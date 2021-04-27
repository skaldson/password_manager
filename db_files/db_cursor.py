#DBCursor class, singleton pattern
import sqlite3
import sys

from cypher_func import generate_hash
from binary_manipulators import binary_to_file, convert_into_binary
from user_info import UserInfo

sys.path.append('.')


class DBCursor:
    __instance = None
    @staticmethod
    def getInstance():
        if DBCursor.__instance == None:
            DBCursor()
        return DBCursor.__instance
    def __init__(self):
        if DBCursor.__instance != None:
            raise Exception("This class is a DBCursor!")
        else:
            DBCursor.__instance = self
            self.set_db_manipulators()


    def set_db_manipulators(self):
        self.__db_name = './db_files/Logins.db'
        self.db_connector = sqlite3.connect(self.__db_name)
        self.db_cursor = self.db_connector.cursor()
        self.user_info = UserInfo.getInstance()
        # self.user_info.user_id = self.user_info.user_id


    def add_new_user(self, name, key, image):
        query = """INSERT INTO `Users`(`Name`, `Key`, `Image`) VALUES
                        (?, ?, ?)"""

        name = generate_hash(name)
        key = generate_hash(key)
        image = convert_into_binary(image)

        data_tuple = (name, key, image)

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

    # def get_user_name_by_id(self):
    #     query = """SELECT `Name` FROM Users WHERE Name=?"""



    def get_user_key_by_id(self):
        query = """SELECT `Key` FROM `Users` WHERE `ID`='%s'""" % (self.user_info.user_id,)

        self.db_cursor.execute(query)
        return (self.db_cursor.fetchall())[0][0]

    # def turn_on_foreign_keys(self, is_on=True):
    #     if is_on:
    #         query = """PRAGMA foreign_keys = ON;"""
    #     else:
    #         query = """PRAGMA foreign_keys = OFF;"""

    #     self.db_cursor.execute(query)
    #     self.db_connector.commit()

    # getters
    @property
    def get_main_key(self):
        query = """SELECT `Parameter Value` FROM `Program Data` WHERE `Parameter`='key'"""

        self.db_cursor.execute(query)
        return self.db_cursor.fetchall()


    @property
    def get_tags_table(self):
        query = """SELECT DISTINCT Tag FROM Tags"""

        self.db_cursor.execute(query)
        result = self.db_cursor.rowcount

        return result

    @property
    def get_tag_and_colour(self):
        query = """SELECT Tag, Colour.Colour FROM Tags, Colour 
                            WHERE Tags.Colour_ID=Colour.ID"""

        self.db_cursor.execute(query)
        return self.db_cursor.fetchall()

    def get_special_tag_and_colour(self, exceptions):
        exceptions = str(exceptions)
        exceptions = exceptions.replace('[', '(')
        exceptions = exceptions.replace(']', ')')
        query = """SELECT Tag, Colour.Colour FROM Tags, Colour 
                            WHERE Tags.Colour_ID=Colour.ID
                                AND Tag NOT IN %s""" % (exceptions)

        self.db_cursor.execute(query)
        return self.db_cursor.fetchall()


    @property
    def get_last_id_login(self):
        query = """SELECT * FROM `Logins`"""

        self.db_cursor.execute(query)
        return len(self.db_cursor.fetchall())

    def get_name_login(self):
        query = """SELECT Logins.Login_Name FROM Logins, Users 
            WHERE Logins.User_ID=Users.ID AND Logins.User_ID='%s'""" % (self.user_info.user_id,)

        self.db_cursor.execute(query)
        return self.db_cursor.fetchall()

    
    def get_intermediate_tag_id(self, tag_name):
        query = """SELECT Intermediate.Tag_ID FROM Tags, Intermediate WHERE 
                    Tags.Id=Intermediate.Tag_ID
                        AND Tags.Tag='%s'""" % (tag_name)
        
        self.db_cursor.execute(query)
        return self.db_cursor.fetchall()

    def get_tags_by_login_name(self, login_name):
        query = """SELECT `Tags`.Tag, `Colour`.Colour FROM `Tags`, `Colour`
                    WHERE  `Tags`.`ID` IN  (SELECT `Tag_ID` 
                        FROM `Intermediate`, `Logins` WHERE 
                            `Intermediate`.`Login_ID`=`Logins`.`ID` AND 
                                `Logins`.`Login_Name`='%s')
                                    AND `Tags`.Colour_ID=Colour.ID""" % (login_name)

        self.db_cursor.execute(query)
        return self.db_cursor.fetchall()

    def get_tag_id_by_name(self, tag_name):
        query = """SELECT Tags.ID FROM Tags WHERE Tags.Tag='%s'""" % (tag_name)

        self.db_cursor.execute(query)
        return (self.db_cursor.fetchall())[0][0]


    @property
    def get_colors(self):
        query = """SELECT Colour.Colour FROM Colour"""

        self.db_cursor.execute(query)
        return self.db_cursor.fetchall()

    def get_colour_by_id(self, colour_id):
        query = """SELECT Colour.Colour FROM Colour WHERE Colour.ID='%s'""" % (colour_id)

        self.db_cursor.execute(query)
        return self.db_cursor.fetchall()

    def get_colour_by_name(self, colour_name):
        query = """SELECT Colour.ID FROM Colour WHERE Colour.Colour='%s'""" % (colour_name)

        self.db_cursor.execute(query)
        return self.db_cursor.fetchall()


    def get_login_id(self, login_name):
        query = """SELECT Logins.ID FROM `Logins` INNER JOIN `Users`
                ON Logins.User_ID=Users.ID WHERE Logins.Login_Name='%s'
                    AND Users.ID='%s'""" % (login_name, self.user_info.user_id,)

        self.db_cursor.execute(query)
        return self.db_cursor.fetchall()

    # REWRITE!!!!!!
    def get_full_user_info(self):
        query = """SELECT Logins.Login_Name, Logins.Login, Logins.Password, Logins.Urandom, Colour.Colour as Colour, Tags.Tag 
                        FROM Logins, Tags, Colour, Users WHERE Users.ID=Logins.User_ID AND User_ID=%s""" % (self.user_info.user_id,)

        self.db_cursor.execute(query)
        return self.db_cursor.fetchall()


    def get_login_id_by_name(self, login_name):
        query = """SELECT Logins.ID FROM `Logins`, `Users` 
            WHERE Logins.User_ID=Users.ID AND Logins.Login_Name='%s' 
                AND Logins.User_ID='%s'""" % (login_name, self.user_info.user_id,)

        self.db_cursor.execute(query)
        return (self.db_cursor.fetchall())[0][0]

    def get_user_photo_by_id(self):
        query = """SELECT Image FROM Users WHERE ID='%s'""" % (self.user_info.user_id,)

        self.db_cursor.execute(query)
        return (self.db_cursor.fetchall())[0][0]

    # manipulators
    def add_record_login(self, login_name, user_login, user_password, urandom):
        query = """INSERT INTO `Logins`(`Login_Name`, `Login`, `Password`, `Urandom`, `User_ID`) VALUES
                    (?, ?, ?, ?, ?)"""
        
        self.db_cursor.execute(query, (login_name, user_login, user_password, urandom, self.user_info.user_id,))
        self.db_connector.commit()

    def add_record_tag(self, login_name, tags):
        login_id = self.get_login_id_by_name(login_name)
        for i in tags:
            current_tag_id = (self.get_tag_id_by_name(i))
            query = """INSERT INTO `Intermediate` 
                (Tag_ID, Login_ID, User_ID) VALUES(%s, %s, %s);""" % (current_tag_id, login_id, self.user_info.user_id)
            self.db_cursor.execute(query)
        
        self.db_connector.commit()

    def add_new_tag(self, tag_name, tag_colour):
        query = """INSERT INTO `Tags` (`Tag`, `Colour_ID`) 
                        VALUES ('%s', '%s')""" % (tag_name, tag_colour)

        self.db_cursor.execute(query)
        self.db_connector.commit()

    # edit tag
    def edit_tag(self, old_name, new_name, tag_colour):
        
        query = """UPDATE `Tags` SET `Tag`='%s', `Colour_ID`='%s' 
                    WHERE `Tag`='%s'""" % (new_name, tag_colour, old_name)

        self.db_cursor.execute(query)
        self.db_connector.commit()

    def delete_tag(self, tag_name):
        query = """DELETE FROM `Tags` WHERE `Tag`='%s'""" % (tag_name)

        self.db_cursor.execute(query)
        self.db_connector.commit()

    def unselect_tag(self, tag_name):
        tag_id = self.get_tag_id_by_name(tag_name)
        query = """DELETE FROM `Intermediate` 
            WHERE Tag_ID='%s' AND User_ID='%s'""" % (tag_id, self.user_info.user_id,)

        self.db_cursor.execute(query)
        self.db_connector.commit()


    def delete_user_record(self, login_id):
        self.db_cursor.execute('BEGIN')
        try:
            delete_intermediate = """DELETE FROM `Intermediate` WHERE Intermediate.User_ID IN 
                (SELECT Users.ID FROM Users INNER JOIN Intermediate ON
	                Intermediate.User_ID=Users.ID WHERE Intermediate.Login_ID='%s' 
                        AND Intermediate.User_ID='%s')""" % (login_id, self.user_info.user_id,)
            delete_record = """DELETE FROM `Logins` WHERE 
                Logins.ID IN (SELECT Logins.ID FROM Logins INNER JOIN Users ON
                    Logins.User_ID=Users.ID WHERE Logins.ID='%s' 
                        AND Users.ID='%s')""" % (login_id, self.user_info.user_id,)
            
            self.db_cursor.execute(delete_intermediate)
            self.db_cursor.execute(delete_record)
        except sqlite3.Error:
            print('failed!')
            print('rollback!')

        self.db_connector.commit()

    def edit_login(self, login_name, login, password, urandom, old_name):
        query = """UPDATE `Logins` SET `Login_Name`=?, `Login`=?, `Password`=?, `Urandom`=? 
                            WHERE `Login_Name`=? AND `User_ID`=?"""

        data_tuple = (login_name, login, password, urandom, old_name, self.user_info.user_id,)
        self.db_cursor.execute(query, data_tuple)
        self.db_connector.commit()

    def get_intermediate_rows_by_user_id(self, login_id):
        query = """SELECT Intermediate.Tag_ID, Intermediate.Login_ID FROM `Intermediate` 
            INNER JOIN `Users` ON `Intermediate`.`User_ID`=`Users`.`ID` 
                WHERE Intermediate.Login_ID='%s' 
                    AND Intermediate.User_ID='%s'""" % (login_id, self.user_info.user_id,)

        self.db_cursor.execute(query)
        return self.db_cursor.fetchall()

    def update_intermediate(self, login_name, tags):
        login_id = self.get_login_id_by_name(login_name)
        available_tags = self.get_intermediate_rows_by_user_id(login_id)
        
        for i in tags:
            tag_id = self.get_tag_id_by_name(i)
            if available_tags:
                temp = (tag_id, login_id)
                if temp in available_tags:
                    continue
                else:
                    query = """INSERT INTO `Intermediate` (Tag_ID, Login_ID, User_ID) 
                        VALUES(%s, %s, %s);""" % (tag_id, login_id, self.user_info.user_id)
            else:
                if [tag_id, login_id] in available_tags:
                    continue
                else:
                    query = """INSERT INTO `Intermediate` (Tag_ID, Login_ID, User_ID) 
                        VALUES(%s, %s, %s);""" % (tag_id, login_id, self.user_info.user_id)

            self.db_cursor.execute(query)    

        self.db_connector.commit()


    def update_user_info(self, new_name, new_passwd, new_photo):
        query = """UPDATE `Users` SET Name=?, Key=?, Image=? 
            WHERE ID=?"""

        data_tuple = (new_name, new_passwd, new_photo, self.user_info.user_id,)

        self.db_cursor.execute(query, data_tuple)
        self.db_connector.commit()

    def get_user_data(self):
        query = """SELECT Name, Key FROM Users
            WHERE ID='%s'""" % (self.user_info.user_id,)

        self.db_cursor.execute(query)
        return (self.db_cursor.fetchall())[0]

    def delete_user(self):
        query_intrmd_del = """DELETE FROM Intermediate WHERE User_ID='%s'""" % (self.user_info.user_id)
        query_logins_del = """DELETE FROM Logins WHERE User_ID='%s'""" % (self.user_info.user_id)
        query_user_del = """DELETE FROM Users WHERE ID='%s'""" % (self.user_info.user_id)

        self.db_cursor.execute('BEGIN')
        try:
            query_list = [query_intrmd_del, query_logins_del, query_user_del]

            for query in query_list:
                self.db_cursor.execute(query)
            self.db_connector.commit()
        except sqlite3.Error:
            print('failed!\nrollback!')
