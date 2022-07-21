import sqlite3


def dbget_latnum(id):
    try:
        sqlite_connection = sqlite3.connect('users.db')
        cursor = sqlite_connection.cursor()
        sqlite_insert_query = """SELECT lastnum
                                FROM users
                                WHERE tele_id = ?;"""
        valuess = (id)
        cursor.execute(sqlite_insert_query, valuess)
        lastnum = cursor.fetchone()
        sqlite_connection.commit()
        print("Пользователь добавлен")
        cursor.close()

    except sqlite3.Error as error:
        print("Ошибка при подключении к sqlite:", error)
        lastnum = -1
    finally:
        if (sqlite_connection):
            sqlite_connection.close()
            print("Соединение с SQLite закрыто")
        return int(lastnum)


def dbadd_user(uid, uname):
    try:
        sqlite_connection = sqlite3.connect('users.db')
        cursor = sqlite_connection.cursor()
        sqlite_insert_query = '''INSERT INTO users
                                (tele_id, name, lastnum)
                                VALUES
                                (?, ?, 0);'''
        valuess = (uid, uname)
        cursor.execute(sqlite_insert_query, valuess)
        sqlite_connection.commit()
        print("Пользователь добавлен")
        cursor.close()

    except sqlite3.Error as error:
        print("Ошибка при подключении к sqlite:", error)
    finally:
        if (sqlite_connection):
            sqlite_connection.close()
            print("Соединение с SQLite закрыто")


def dbadd_pic(id, uid):
    try:
        sqlite_connection = sqlite3.connect('pics.db')
        cursor = sqlite_connection.cursor()
        sqlite_insert_query = '''INSERT INTO pics
                                (id, user_id, rate)
                                VALUES
                                (?, ?, 0);'''
        valuess = (id, uid)
        cursor.execute(sqlite_insert_query, valuess)
        sqlite_connection.commit()
        print("Картинка добавлена")
        cursor.close()

    except sqlite3.Error as error:
        print("Ошибка при подключении к sqlite:", error)
    finally:
        if (sqlite_connection):
            sqlite_connection.close()
            print("Соединение с SQLite закрыто")


def setup_users():
    try:
        sqlite_connection = sqlite3.connect('users.db')
        sqlite_create_table_query = """CREATE TABLE users(
                    id INTEGER UNIQUE PRIMARY KEY,
                    tele_id INTEGER UNIQUE NOT NULL,
                    name TEXT,
                    lastnum INTEGER);"""
        cursor = sqlite_connection.cursor()
        cursor.execute(sqlite_create_table_query)
        sqlite_connection.commit()
        print("Таблица пользователей создана")
        cursor.close()

    except sqlite3.Error as error:
        print("Ошибка при подключении к sqlite:", error)
    finally:
        if (sqlite_connection):
            sqlite_connection.close()
            print("Соединение с SQLite закрыто")


def setup_pics():
    try:
        sqlite_connection = sqlite3.connect('pics.db')
        #sqlite_connection1 = sqlite3.connect('users.db')
        sqlite_create_table_query = """CREATE TABLE pics(
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            user_id INTEGER,
                            rate INTEGER,
                            FOREIGN KEY (user_id) REFERENCES users(tele_id) );"""
        cursor = sqlite_connection.cursor()
        cursor.execute(sqlite_create_table_query)
        sqlite_connection.commit()
        print("Таблица картинок создана")
        cursor.close()

    except sqlite3.Error as error:
        print("Ошибка при подключении к sqlite:", error)
    finally:
        if (sqlite_connection):
            sqlite_connection.close()
            #sqlite_connection1.close()
            print("Соединение с SQLite закрыто")