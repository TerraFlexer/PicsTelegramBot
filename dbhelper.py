import sqlite3


def dbget_lastnum(uid):
    try:
        sqlite_connection = sqlite3.connect('users.db')
        cursor = sqlite_connection.cursor()
        sqlite_select_query = """SELECT lastnum
                                FROM users
                                WHERE tele_id = ?;"""
        cursor.execute(sqlite_select_query, (uid,))
        lastnum = cursor.fetchone()
        print("dbgetlastnum: Значение получено ", lastnum[0])
        cursor.close()
        return lastnum[0]

    except sqlite3.Error as error:
        print("getlastnum: Ошибка при подключении к sqlite:", error)
    finally:
        if (sqlite_connection):
            sqlite_connection.close()
            print("dbgetlastnum: Соединение с SQLite закрыто")


def dbupdate_lastnum(uid, newlnum):
    try:
        sqlite_connection = sqlite3.connect('users.db')
        cursor = sqlite_connection.cursor()
        sqlite_update_query = '''UPDATE users
                                SET lastnum = ?
                                WHERE tele_id = ?;'''
        valuess = (newlnum, uid)
        cursor.execute(sqlite_update_query, valuess)
        sqlite_connection.commit()
        print("dbupdate_lastnum: Запись изменена")
        cursor.close()

    except sqlite3.Error as error:
        print("dbupdate_lastnum: Ошибка при подключении к sqlite:", error)
    finally:
        if (sqlite_connection):
            sqlite_connection.close()
            print("dbupdate_lastnum: Соединение с SQLite закрыто")


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


def dbget_rating(pid):
    try:
        sqlite_connection = sqlite3.connect('pics.db')
        cursor = sqlite_connection.cursor()
        sqlite_select_query = """SELECT rate
                                FROM pics
                                WHERE id = ?;"""
        cursor.execute(sqlite_select_query, (pid,))
        rating = cursor.fetchone()
        print("dbgetrating: Значение получено ", rating[0])
        cursor.close()
        return rating[0]

    except sqlite3.Error as error:
        print("dbgetrating: Ошибка при подключении к sqlite:", error)
    finally:
        if (sqlite_connection):
            sqlite_connection.close()
            print("dbgetrating: Соединение с SQLite закрыто")


def dbupdate_rating(uid, pid, rate):
    try:
        sqlite_connection = sqlite3.connect('pics.db')
        cursor = sqlite_connection.cursor()
        currate = dbget_rating(pid)
        sqlite_update_query = '''UPDATE pics
                                SET rate = ?
                                WHERE id = ?;'''
        valuess = (currate + rate, pid)
        cursor.execute(sqlite_update_query, valuess)
        sqlite_connection.commit()
        print("dbupdate_rating: Запись изменена")
        cursor.close()

    except sqlite3.Error as error:
        print("dbupdate_rating: Ошибка при подключении к sqlite:", error)
    finally:
        if (sqlite_connection):
            sqlite_connection.close()
            print("dbupdate_rating: Соединение с SQLite закрыто")


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