# Init Program Database
import sqlite3


class InItDb:
    def __init__(self):
        self.__db_name = './db_files/Logins.db'
        self.db_connector = sqlite3.connect(self.__db_name)
        self.db_cursor = self.db_connector.cursor()

    def __allow_foreign_key(self):
        query = """PRAGMA foreign_keys = ON;"""

        self.db_cursor.execute(query)
        self.db_connector.commit()

    # tables creating
    def __create_program_table(self):
        query = """CREATE TABLE IF NOT EXISTS `Users`(
            `ID` INTEGER PRIMARY KEY AUTOINCREMENT,
            `Name` BLOB NOT NULL,
            `Key` BLOB NOT NULL,
            `Image` BLOB NOT NULL,
            `Urandom` BLOB NOT NULL
        );"""

        self.db_cursor.execute(query)
        self.db_connector.commit()

    def __create_logins_table(self):
        query_create_logins = """CREATE TABLE IF NOT EXISTS `Logins`(
            `ID` INTEGER PRIMARY KEY AUTOINCREMENT,
            `Login_Name` BLOB NOT NULL,
            `Login` BLOB NOT NULL,
            `Password` BLOB NOT NULL,
            `Urandom` BLOB NOT NULL,
            `User_ID` INTEGER NOT NULL,
            FOREIGN KEY(`User_ID`) REFERENCES `Users`(`ID`));"""

        self.db_cursor.execute(query_create_logins)
        self.db_connector.commit()

    def __create_tags_table(self):
        query_create_table = """CREATE TABLE IF NOT EXISTS `Tags`(
            `ID` INTEGER PRIMARY KEY AUTOINCREMENT,
            `Tag` TEXT NOT NULL,
            `Colour_ID` INTEGER NOT NULL,
            FOREIGN KEY(`Colour_ID`) REFERENCES `Colour`(`ID`));"""

        self.db_cursor.execute(query_create_table)
        self.db_connector.commit()

    def __create_intermediate_table(self):
        query_create_table = """CREATE TABLE IF NOT EXISTS `Intermediate`(
            `ID` INTEGER PRIMARY KEY AUTOINCREMENT,
            `Tag_ID` INTEGER,
            `Login_ID` INTEGER NOT NULL,
            `User_ID` INTEGER NOT NULL,
            FOREIGN KEY(`Tag_ID`) REFERENCES `Tags`(`ID`)
            FOREIGN KEY(`Login_ID`) REFERENCES `Logins`(`ID`)
            FOREIGN KEY(`User_ID`) REFERENCES `Users`(`ID`));"""

        self.db_cursor.execute(query_create_table)
        self.db_connector.commit()

    def __create_colour_table(self):
        query_create_table = """CREATE  TABLE IF NOT EXISTS `Colour` (
                            `ID` INTEGER PRIMARY KEY,
                            `Colour` TEXT NOT NULL);"""

        self.db_cursor.execute(query_create_table)
        self.db_connector.commit()

    # insert some initial data
    def __insert_into_colour(self):
        query_insert = """INSERT INTO `Colour` VALUES
                            (1, 'red'),
                            (2, 'orange'),
                            (3, 'blue'),
                            (4, 'purple'),
                            (5, 'brown'),
                            (6, 'green'),
                            (7, 'yellow'),
                            (8, 'coral'),
                            (9, 'magenta');"""

        self.db_cursor.execute(query_insert)
        self.db_connector.commit()

    def __insert_into_tags(self):
        query_insert = """INSERT INTO `Tags`(`ID`, `Tag`, `Colour_ID`) VALUES
                            (1, 'facebook', 3),
                            (2, 'twitter', 3),
                            (3, 'reddit', 2),
                            (4, 'personal', 6),
                            (5, 'mail', 1);"""

        self.db_cursor.execute(query_insert)
        self.db_connector.commit()

    # init program database
    def init_db(self):
        self.__allow_foreign_key()
        self.__create_program_table()
        self.__create_logins_table()
        self.__create_colour_table()
        self.__insert_into_colour()
        self.__create_tags_table()
        self.__create_intermediate_table()
        self.__insert_into_tags()


def init_db():
    db_initializer = InItDb()

    try:
        db_initializer.init_db()
    except sqlite3.IntegrityError:
        pass
