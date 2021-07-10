#!/usr/bin/env python3

import os
import sqlite3
import argparse
import db
import user
import datetime
import util


def main():
    args = get_args()
    db_file = args.db_name
    remove_db_if_exists(db_file)
    try:
        run_test(test_setup_database, "Setup Database", db_file)
        run_test(test_insert_get_all_user, "Insert and Get All User", db_file)
    except AssertionError as e:
        print("Failed")
        if (args.verbose):
            print(e.with_traceback())
    finally:
        remove_db_if_exists(db_file)

def get_args():
    parser = argparse.ArgumentParser("Test api")
    parser.add_argument("--db-name", default="test.db", type=str)
    parser.add_argument("--verbose", action="store_true")
    return parser.parse_args()

def remove_db_if_exists(db_file):
    try:
        os.remove(db_file)
    except:
        pass

def run_test(func, name, *args):
    print("Testing {}".format(name))
    func(*args)
    print("Passed")
    

def test_setup_database(db_file):
    db.setup_database(db_file)
    assert(os.path.isfile(db_file))
    with db.get_connection(db_file) as conn:
        cursor = conn.cursor()
        cursor.execute(
            '''
            SELECT name FROM sqlite_master WHERE type='table'
            '''
        )
        tables = [row[0] for row in cursor.fetchall()]
        assert len(tables) == 2
        assert "user" in tables
        assert "listing" in tables

def test_insert_get_all_user(db_file):
    username_base = "test_"
    name = "Test User"
    password = "password"
    salt = "abcdefg"
    token = "abcdefg"
    insert_user = user.ClientUser(username_base + "client", name, datetime.datetime.now(), util.get_hash(salt + password), salt, token)
    db.insert_user(insert_user, db_file=db_file)
    users = db.get_all_users(db_file=db_file)
    assert len(users) == 1
    assert type(users[0]) == user.ClientUser
    insert_user = user.RealtorUser(username_base + "realtor", name, datetime.datetime.now(), util.get_hash(salt + password), salt, token)
    db.insert_user(insert_user, db_file=db_file)
    users = db.get_all_users(db_file=db_file)
    assert len(users) == 2
    assert type(users[1]) == user.RealtorUser
    insert_user = user.AdminUser(username_base + "admin", name, datetime.datetime.now(), util.get_hash(salt + password), salt, token)
    db.insert_user(insert_user, db_file=db_file)
    users = db.get_all_users(db_file=db_file)
    assert len(users) == 3
    assert type(users[2]) == user.AdminUser

if __name__ == "__main__":
    main()
