#DBCursor class, singleton pattern
import sqlite3


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

    def init_main_key(self, main_key):
        query = """INSERT INTO `Program Data`(`Parameter`, `Parameter Value`) VALUES
                        ('key', '%s')""" % (main_key)

        self.db_cursor.execute(query)
        self.db_connector.commit()

    def turn_on_foreign_keys(self, is_on=True):
        if is_on:
            query = """PRAGMA foreign_keys = ON;"""
        else:
            query = """PRAGMA foreign_keys = OFF;"""

        self.db_cursor.execute(query)
        self.db_connector.commit()

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


    @property
    def get_last_id_login(self):
        query = """SELECT * FROM `Logins`"""

        self.db_cursor.execute(query)
        return len(self.db_cursor.fetchall())

    @property
    def get_name_login(self):
        query = """SELECT Logins.Login_Name FROM Logins"""

        self.db_cursor.execute(query)
        return self.db_cursor.fetchall()


    @property
    def get_colors(self):
        query = """SELECT Colour.Colour FROM Colour"""

        self.db_cursor.execute(query)
        return self.db_cursor.fetchall()

    def get_colour_by_id(self, colour_id):
        query = """SELECT Colour.Colour FROM Colour WHERE Colour.ID=%s""" % (colour_id)

        self.db_cursor.execute(query)
        return self.db_cursor.fetchall()

    def get_colour_by_name(self, colour_name):
        query = """SELECT Colour.ID FROM Colour WHERE Colour.Colour='%s'""" % (colour_name)

        self.db_cursor.execute(query)
        return self.db_cursor.fetchall()

    @property
    def get_full_user_info(self):
        query = """SELECT Logins.Login_Name, Logins.Login, Logins.Password, Logins.Urandom, Colour.Colour as Colour, Tags.Tag 
                        FROM Logins, Tags, Colour, Intermediate WHERE Intermediate.Login_ID=Logins.ID 
                            AND Intermediate.Tag_ID=Tags.ID AND Tags.Colour_ID=Colour.ID """

        self.db_cursor.execute(query)
        return self.db_cursor.fetchall()


    # manipulators
    def add_record_login(self, login_name, user_login, user_password, urandom):
        query = """INSERT INTO `Logins`(`Login_Name`, `Login`, `Password`, `Urandom`) VALUES
                    (?, ?, ?, ?)"""
        
        self.db_cursor.execute(query, (login_name, user_login, user_password, urandom))
        self.db_connector.commit()

    def add_record_tag(self, tags):
        login_id = (self.get_last_id_login + 1)
        
        for i in tags:
            query = """INSERT INTO `Intermediate`(`Tag_ID`, `Login_ID`) VALUES
                        (%s, %s)""" % (i, login_id)
            self.db_cursor.execute(query)
            self.db_connector.commit()

    def add_new_tag(self, tag_name, tag_colour):
        query = """INSERT INTO `Tags` (`Tag`, `Colour_ID`) VALUES ('%s', '%s')""" % (tag_name, tag_colour)

        self.db_cursor.execute(query)
        self.db_connector.commit()

    # edit tag
    def edit_tag(self, tag_index, tag_name, tag_colour):
        
        query = """UPDATE `Tags` SET `Tag`='%s', `Colour_ID`='%s' WHERE `ID`='%s'""" % (tag_name, tag_colour, tag_index)

        self.db_cursor.execute(query)
        self.db_connector.commit()

    def delete_tag(self, tag_index):
        tag_index += 1
        query = """DELETE FROM `Tags` WHERE `ID`='%s'""" % (tag_index)

        self.db_cursor.execute(query)
        self.reinit_tags_table()

    
    def reinit_tags_table(self):
        query = """SELECT * FROM `Tags`"""
        
        tags_sqlite_obj = self.db_cursor.execute(query)
        tags_content = tags_sqlite_obj.fetchall()
        query_truncate = 'DELETE FROM Tags;'
        self.db_cursor.execute(query_truncate)
        self.db_connector.commit()
        
        for i in range(len(tags_content)):
            query_insert = """INSERT INTO `Tags` (`ID`, `Tag`, `Colour_ID`) VALUES (?, ?, ?)"""
            self.db_cursor.execute(query_insert, (i+1, tags_content[i][1], tags_content[i][-1]))
        self.db_connector.commit()
