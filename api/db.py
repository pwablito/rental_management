import sqlite3
import datetime
import dateutil.parser
import user
import error
import listing


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
                password_salt TEXT NOT NULL,
                token TEXT
            )
            '''
        )
        cursor.execute(
            '''
            CREATE TABLE listing (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                description TEXT NOT NULL,
                floor_area REAL NOT NULL,
                price REAL NOT NULL,
                rooms INTEGER NOT NULL,
                bathrooms INTEGER NOT NULL,
                created_on INTEGER NOT NULL,
                latitude REAL NOT NULL,
                longitude REAL NOT NULL,
                is_listed INTEGER NOT NULL
            )
            '''
        )


def get_user(username):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            '''
            SELECT username, name, created_on, type,
            password_hash, password_salt, token
            FROM user WHERE username=?
            ''', (username,)
        )
        row = cursor.fetchone()
        if not row:
            raise error.UserNotFoundException
        entry = user.User(row[0], row[1], dateutil.parser.parse(
            row[2]), row[4], row[5], row[6])
        if row[3] == CLIENT_TYPE:
            return user.ClientUser(
                entry.username,
                entry.name,
                entry.created_on,
                entry.password_hash,
                entry.password_salt,
                entry.token
            )
        elif row[3] == REALTOR_TYPE:
            return user.RealtorUser(
                entry.username,
                entry.name,
                entry.created_on,
                entry.password_hash,
                entry.password_salt,
                entry.token
            )
        elif row[3] == ADMIN_TYPE:
            return user.AdminUser(
                entry.username,
                entry.name,
                entry.created_on,
                entry.password_hash,
                entry.password_salt,
                entry.token
            )
        raise InvalidUserTypeException

def get_user_by_token(token):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            '''
            SELECT username, name, created_on, type,
            password_hash, password_salt, token
            FROM user WHERE token=?
            ''', (token,)
        )
        row = cursor.fetchone()
        if not row:
            raise error.UserNotFoundException
        entry = user.User(row[0], row[1], dateutil.parser.parse(
            row[2]), row[4], row[5], row[6])
        if row[3] == CLIENT_TYPE:
            return user.ClientUser(
                entry.username,
                entry.name,
                entry.created_on,
                entry.password_hash,
                entry.password_salt,
                entry.token
            )
        elif row[3] == REALTOR_TYPE:
            return user.RealtorUser(
                entry.username,
                entry.name,
                entry.created_on,
                entry.password_hash,
                entry.password_salt,
                entry.token
            )
        elif row[3] == ADMIN_TYPE:
            return user.AdminUser(
                entry.username,
                entry.name,
                entry.created_on,
                entry.password_hash,
                entry.password_salt,
                entry.token
            )
        raise InvalidUserTypeException


def get_user_type_number(user_to_evaluate):
    if type(user_to_evaluate) == user.ClientUser:
        return CLIENT_TYPE
    if type(user_to_evaluate) == user.RealtorUser:
        return REALTOR_TYPE
    if type(user_to_evaluate) == user.AdminUser:
        return ADMIN_TYPE
    raise error.InvalidUserTypeException


def insert_user(entry):
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                '''
                INSERT INTO user (username, name, created_on,
                type, password_hash, password_salt, token)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (
                    entry.username,
                    entry.name,
                    entry.created_on,
                    get_user_type_number(entry),
                    entry.password_hash,
                    entry.password_salt,
                    entry.token,
                )
            )
    except sqlite3.IntegrityError:
        raise error.UserAlreadyExistsException


def update_token(username, token):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            '''
            UPDATE user SET token=? WHERE username=?
            ''', (token, username,)
        )


def get_all_listings(only_listed=False):
    query_string = '''
                    SELECT id, name, description, floor_area, price,
                    rooms, bathrooms, created_on, latitude, longitude, is_listed
                    FROM listing
                    '''
    if only_listed:
        query_string += '''
                        WHERE is_listed=1
                        '''
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(query_string)
        rows = cursor.fetchall()
        listings = []
        for row in rows:
            listings.append(listing.Listing(
                row[0],
                row[1],
                row[2],
                row[3],
                row[4],
                row[5],
                row[6],
                dateutil.parser.parse(row[7]),
                row[8],
                row[9],
                True if row[10] != 0 else False,
            ))
        return listings


def insert_listing(listing):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            '''
            INSERT INTO listing (id, name, description, floor_area,
            price, rooms, bathrooms, created_on, latitude, longitude, is_listed)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                listing.id,
                listing.name,
                listing.description,
                listing.floor_area,
                listing.price,
                listing.rooms,
                listing.bathrooms,
                listing.created_on,
                listing.latitude,
                listing.longitude,
                1 if listing.is_listed else 0
            )
        )


def delete_listing(id):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            '''
            DELETE FROM listing WHERE id=?
            ''', (id,)
        )


def delete_user(username):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            '''
            DELETE FROM user WHERE username=?
            ''', (username,)
        )


def get_all_users():
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            '''
            SELECT username, name, created_on, type,
            password_hash, password_salt, token
            FROM user
            '''
        )
        rows = cursor.fetchall()
        users = []
        for row in rows:
            entry = user.User(row[0], row[1], dateutil.parser.parse(
                row[2]), row[4], row[5], row[6])
            if row[3] == CLIENT_TYPE:
                return user.ClientUser(
                    entry.username,
                    entry.name,
                    entry.created_on,
                    entry.password_hash,
                    entry.password_salt,
                    entry.token
                )
            elif row[3] == REALTOR_TYPE:
                return user.RealtorUser(
                    entry.username,
                    entry.name,
                    entry.created_on,
                    entry.password_hash,
                    entry.password_salt,
                    entry.token
                )
            elif row[3] == ADMIN_TYPE:
                return user.AdminUser(
                    entry.username,
                    entry.name,
                    entry.created_on,
                    entry.password_hash,
                    entry.password_salt,
                    entry.token
                )
            raise InvalidUserTypeException
            users.append(entry)
        return users
