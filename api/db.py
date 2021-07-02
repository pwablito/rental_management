import sqlite3


CLIENT_TYPE = 1
REALTOR_TYPE = 2
ADMIN_TYPE = 3

def get_connection(db_file):
    try:
        return sqlite3.connect(db_file)
    except sqlite3.Error as e:
        print("Unable to connect to database: {}".format(e))

def setup_database():
    with get_connection("db.sqlite") as conn:
        cursor = conn.cursor()
        cursor.execute(
            '''
            CREATE TABLE user (
                id AUTO PRIMARY KEY,
                username TEXT NOT NULL,
                name TEXT NOT NULL,
                created_on INTEGER NOT NULL,
                type INTEGER NOT NULL,
                password_hash TEXT NOT NULL,
                password_salt TEXT NOT NULL
            )
            '''
        )
        cursor.execute(
            '''
            CREATE TABLE listing (
                id AUTO PRIMARY KEY,
                name TEXT NOT NULL,
                description TEXT NOT NULL,
                floor_area REAL NOT NULL,
                price REAL NOT NULL,
                rooms INTEGER NOT NULL,
                bathrooms INTEGER NOT NULL,
                created_on INTEGER NOT NULL,
                latitude REAL NOT NULL,
                longitude REAL NOT NULL
            )
            '''
        )