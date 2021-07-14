import sqlite3
import datetime
import dateutil.parser
import user
import error
import listing


CLIENT_TYPE = 1
REALTOR_TYPE = 2
ADMIN_TYPE = 3


def get_connection(db_file):
    try:
        return sqlite3.connect(db_file)
    except sqlite3.Error as e:
        print("Unable to connect to database: {}".format(e))


def setup_database(db_file="db.sqlite"):
    with get_connection(db_file) as conn:
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
                token TEXT,
                token_created TEXT
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
                is_listed INTEGER NOT NULL,
                realtor TEXT NOT NULL
            )
            '''
        )


def get_user(username, db_file="db.sqlite"):
    with get_connection(db_file) as conn:
        cursor = conn.cursor()
        cursor.execute(
            '''
            SELECT username, name, created_on, type,
            password_hash, password_salt, token, token_created
            FROM user WHERE username=?
            ''', (username,)
        )
        row = cursor.fetchone()
        if not row:
            raise error.UserNotFoundException
        entry = user.User(row[0], row[1], dateutil.parser.parse(row[2]), row[4], row[5], row[6], dateutil.parser.parse(row[7]) if row[7] else None)
        if row[3] == CLIENT_TYPE:
            return user.ClientUser(
                entry.username,
                entry.name,
                entry.created_on,
                entry.password_hash,
                entry.password_salt,
                entry.token,
                entry.token_created,
            )
        elif row[3] == REALTOR_TYPE:
            return user.RealtorUser(
                entry.username,
                entry.name,
                entry.created_on,
                entry.password_hash,
                entry.password_salt,
                entry.token,
                entry.token_created,
            )
        elif row[3] == ADMIN_TYPE:
            return user.AdminUser(
                entry.username,
                entry.name,
                entry.created_on,
                entry.password_hash,
                entry.password_salt,
                entry.token,
                entry.token_created,
            )
        raise InvalidUserTypeException

def get_user_by_token(token, db_file="db.sqlite"):
    with get_connection(db_file) as conn:
        cursor=conn.cursor()
        cursor.execute(
            '''
            SELECT username, name, created_on, type,
            password_hash, password_salt, token, token_created
            FROM user WHERE token=?
            ''', (token,)
        )
        row = cursor.fetchone()
        if not row:
            raise error.UserNotFoundException
        entry=user.User(row[0], row[1], dateutil.parser.parse(
            row[2]), row[4], row[5], row[6], dateutil.parser.parse(row[7]) if row[7] else None)
        if row[3] == CLIENT_TYPE:
            return user.ClientUser(
                entry.username,
                entry.name,
                entry.created_on,
                entry.password_hash,
                entry.password_salt,
                entry.token,
                entry.token_created,
            )
        elif row[3] == REALTOR_TYPE:
            return user.RealtorUser(
                entry.username,
                entry.name,
                entry.created_on,
                entry.password_hash,
                entry.password_salt,
                entry.token,
                entry.token_created,
            )
        elif row[3] == ADMIN_TYPE:
            return user.AdminUser(
                entry.username,
                entry.name,
                entry.created_on,
                entry.password_hash,
                entry.password_salt,
                entry.token,
                entry.token_created,
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


def insert_user(entry, db_file="db.sqlite"):
    try:
        with get_connection(db_file) as conn:
            cursor=conn.cursor()
            cursor.execute(
                '''
                INSERT INTO user (username, name, created_on,
                type, password_hash, password_salt)
                VALUES (?, ?, ?, ?, ?, ?)
                ''', (
                    entry.username,
                    entry.name,
                    entry.created_on,
                    get_user_type_number(entry),
                    entry.password_hash,
                    entry.password_salt,
                )
            )
    except sqlite3.IntegrityError:
        raise error.UserAlreadyExistsException


def set_token(username, token, db_file="db.sqlite"):
    with get_connection(db_file) as conn:
        cursor=conn.cursor()
        cursor.execute(
            '''
            UPDATE user SET token=?, token_created=? WHERE username=?
            ''', (token, datetime.datetime.now(), username,)
        )


def get_all_listings(only_listed=False, db_file="db.sqlite"):
    query_string='''
                    SELECT id, name, description, floor_area, price,
                    rooms, bathrooms, created_on, latitude, longitude,
                    is_listed, realtor
                    FROM listing
                    '''
    if only_listed:
        query_string += '''
                        WHERE is_listed=1
                        '''
    with get_connection(db_file) as conn:
        cursor=conn.cursor()
        cursor.execute(query_string)
        rows=cursor.fetchall()
        listings=[]
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
                row[11],
            ))
        return listings

def get_listing_by_id(listing_id, db_file="db.sqlite"):
    with get_connection(db_file) as conn:
        cursor = conn.cursor()
        cursor.execute(
            '''
            SELECT id, name, description, floor_area, price,
            rooms, bathrooms, created_on, latitude, longitude,
            is_listed, realtor
            FROM listing
            WHERE id=?
            ''', (listing_id,)
        )
        row = cursor.fetchone()
        if not row:
            raise error.ListingNotFoundException
        return listing.Listing(
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
            row[11],
        )

def insert_listing(listing, db_file="db.sqlite"):
    with get_connection(db_file) as conn:
        cursor=conn.cursor()
        cursor.execute(
            '''
            INSERT INTO listing (id, name, description, floor_area,
            price, rooms, bathrooms, created_on, latitude, longitude,
            is_listed, realtor)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
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
                1 if listing.is_listed else 0,
                listing.realtor,
            )
        )


def delete_listing(id, db_file="db.sqlite"):
    with get_connection(db_file) as conn:
        cursor=conn.cursor()
        cursor.execute(
            '''
            DELETE FROM listing WHERE id=?
            ''', (id,)
        )
        conn.commit()


def delete_user(username, db_file="db.sqlite"):
    with get_connection(db_file) as conn:
        cursor=conn.cursor()
        cursor.execute(
            '''
            DELETE FROM user WHERE username=?
            ''', (username,)
        )


def get_all_users(db_file="db.sqlite"):
    with get_connection(db_file) as conn:
        cursor=conn.cursor()
        cursor.execute(
            '''
            SELECT username, name, created_on, type,
            password_hash, password_salt, token, token_created
            FROM user
            '''
        )
        rows=cursor.fetchall()
        users=[]
        for row in rows:
            entry=user.User(row[0], row[1], dateutil.parser.parse(
                row[2]), row[4], row[5], row[6], dateutil.parser.parse(row[7]) if row[7] else None)
            if row[3] == CLIENT_TYPE:
                users.append(user.ClientUser(
                    entry.username,
                    entry.name,
                    entry.created_on,
                    entry.password_hash,
                    entry.password_salt,
                    entry.token,
                    entry.token_created,
                ))
            elif row[3] == REALTOR_TYPE:
                users.append(user.RealtorUser(
                    entry.username,
                    entry.name,
                    entry.created_on,
                    entry.password_hash,
                    entry.password_salt,
                    entry.token,
                    entry.token_created,
                ))
            elif row[3] == ADMIN_TYPE:
                users.append(user.AdminUser(
                    entry.username,
                    entry.name,
                    entry.created_on,
                    entry.password_hash,
                    entry.password_salt,
                    entry.token,
                    entry.token_created,
                ))
            else:
                raise InvalidUserTypeException
        return users

def update_user(entry, db_file="db.sqlite"):
    with get_connection(db_file) as conn:
        cursor=conn.cursor()
        cursor.execute(
            '''
            UPDATE user SET name=?, type=?
            WHERE username=?
            ''', (
                entry.name,
                get_user_type_number(entry),
                entry.username,
            )
        )
def set_user_password(username, password_hash, password_salt, db_file="db.sqlite"):
    with get_connection(db_file) as conn:
        cursor = conn.cursor()
        cursor.execute(
            '''
            UPDATE user SET password_hash=?, password_salt=?
            WHERE username=?
            ''', (
                password_hash,
                password_salt,
                username,
            )
        )

def update_listing(listing, db_file="db.sqlite"):
    with get_connection(db_file) as conn:
        cursor=conn.cursor()
        cursor.execute(
            '''
            UPDATE listing SET name=?, description=?, floor_area=?, price=?,
            rooms=?, bathrooms=?, latitude=?, longitude=?, is_listed=?, realtor=?
            WHERE id=?
            ''', (listing.name, listing.description, listing.floor_area, listing.price,
                  listing.rooms, listing.bathrooms, listing.latitude, listing.longitude,
                  1 if listing.is_listed else 0, listing.realtor, listing.id,)
        )
