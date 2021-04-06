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

    @property
    def get_name_login(self):
        query = """SELECT Logins.Login_Name FROM Logins"""

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
        # print(self.db_cursor.fetchall())
        return self.db_cursor.fetchall()

    def get_colour_by_id(self, colour_id):
        query = """SELECT Colour.Colour FROM Colour WHERE Colour.ID='%s'""" % (colour_id)

        self.db_cursor.execute(query)
        # print(self.db_cursor.fetchall())
        return self.db_cursor.fetchall()

    def get_colour_by_name(self, colour_name):
        query = """SELECT Colour.ID FROM Colour WHERE Colour.Colour='%s'""" % (colour_name)

        self.db_cursor.execute(query)
        return self.db_cursor.fetchall()


    def get_login_id(self, login_name):
        query = """SELECT Logins.ID FROM `Logins` WHERE Logins.Login_Name='%s'""" % (login_name)

        self.db_cursor.execute(query)
        return self.db_cursor.fetchall()

    # REWRITE!!!!!!
    @property
    def get_full_user_info(self):
        query = """SELECT Logins.Login_Name, Logins.Login, Logins.Password, Logins.Urandom, Colour.Colour as Colour, Tags.Tag 
                        FROM Logins, Tags, Colour"""
        # WHERE Intermediate.Login_ID=Logins.ID 
        #                    OR Intermediate.Tag_ID=Tags.ID OR Tags.Colour_ID=Colour.ID

        self.db_cursor.execute(query)
        return self.db_cursor.fetchall()


    def get_login_id_by_name(self, login_name):
        query = """SELECT Logins.ID FROM `Logins` WHERE Logins.Login_Name='%s'""" % (login_name)

        self.db_cursor.execute(query)
        return (self.db_cursor.fetchall())[0][0]

    # manipulators
    def add_record_login(self, login_name, user_login, user_password, urandom):
        query = """INSERT INTO `Logins`(`Login_Name`, `Login`, `Password`, `Urandom`) VALUES
                    (?, ?, ?, ?)"""
        
        self.db_cursor.execute(query, (login_name, user_login, user_password, urandom))
        self.db_connector.commit()

    def add_record_tag(self, login_name, tags):
        login_id = self.get_login_id_by_name(login_name)
        for i in tags:
            current_tag_id = (self.get_tag_id_by_name(i))
            query = """INSERT INTO `Intermediate` (Tag_ID, Login_ID) VALUES(%s, %s);""" % (current_tag_id, login_id)
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
        query = """DELETE FROM `Intermediate` WHERE Tag_ID='%s'""" % (tag_id)

        self.db_cursor.execute(query)
        self.db_connector.commit()


    def delete_login(self, login_id):
        self.db_cursor.execute('BEGIN')
        try:
            self.db_cursor.execute("""DELETE FROM `Intermediate` WHERE Login_ID='%s'""" % (login_id))
            self.db_cursor.execute("""DELETE FROM `Logins` WHERE ID='%s'""" % (login_id))
        except sqlite3.Error:
            print('failed!')
            print('rollback!')

        self.db_connector.commit()

    def edit_login(self, login_name, login, password, urandom, old_name):
        query = """UPDATE `Logins` SET `Login_Name`=?, `Login`=?, `Password`=?, `Urandom`=? 
                            WHERE `Login_Name`=?"""
        print(query)
        self.db_cursor.execute(query, (login_name, login, password, urandom, old_name))
        self.db_connector.commit()

    def get_intermediate_rows_by_login_id(self, login_id):
        query = """SELECT Tag_ID, Login_ID FROM `Intermediate` WHERE Login_ID='%s'""" % (login_id)

        self.db_cursor.execute(query)
        return self.db_cursor.fetchall()

    def update_intermediate(self, login_name, tags):
        login_id = self.get_login_id_by_name(login_name)
        available_tags = self.get_intermediate_rows_by_login_id(login_id)
        print(login_id,': ', tags)
        # print("FUCK1")
        for i in tags:
            tag_id = self.get_tag_id_by_name(i)
            if available_tags:
                print(available_tags)
                temp = (tag_id, login_id)
                if temp in available_tags:
                    continue
                else:
                    query = """INSERT INTO `Intermediate` (Tag_ID, Login_ID) VALUES(%s, %s);""" % (tag_id, login_id)
            else:
                if [tag_id, login_id] in available_tags:
                    continue
                else:
                    query = """INSERT INTO `Intermediate` (Tag_ID, Login_ID) VALUES(%s, %s);""" % (tag_id, login_id)

            self.db_cursor.execute(query)   
            # print(query)    

        self.db_connector.commit()
