import sqlite3
import api.user
import api.error


CLIENT_TYPE = 1
REALTOR_TYPE = 2
ADMIN_TYPE = 3

def get_connection(db_file="db.sqlite"):
    try:
        return sqlite3.connect(db_file)
    except sqlite3.Error as e:
        print("Unable to connect to database: {}".format(e))

def setup_database():
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            '''
            CREATE TABLE user (
                username TEXT PRIMARY KEY,
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

def get_user(username):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        '''
        SELECT username, name, created_on, type, password_hash, password_salt
        FROM user WHERE username=?
        ''', (username,)
    )
    row = cursor.fetchone()
    if not row:
        raise api.error.UserNotFoundException
    user = api.user.User(row[0], row[1], row[2], row[4], row[5])
    if row[3] == CLIENT_TYPE:
        return api.user.ClientUser(user)
    elif row[3] == REALTOR_TYPE:
        return api.user.RealtorUser(user)
    elif row[3] == ADMIN_TYPE:
        return api.user.AdminUser(user)
    raise InvalidUserTypeException

def get_user_type_number(user):
    if type(user) == api.user.ClientUser:
        return CLIENT_TYPE
    if type(user) == api.user.RealtorUser:
        return REALTOR_TYPE
    if type(user) == api.user.AdminType:
        return ADMIN_TYPE
    raise api.error.InvalidUserTypeException

def insert_user(user):
    # try:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        '''
        INSERT INTO user (username, name, created_on, type, password_hash, password_salt)
        VALUES (?, ?, ?, ?, ?, ?)
        ''', (user.username, user.name, user.created_on, get_user_type_number(user), user.password_hash, user.password_salt)
    )
    # except:  # TODO catch conflicting primary keys, throw custom exception
    #     pass