#!/usr/bin/env python3

import argparse
import sqlite3
import datetime
import db
import user
import util


def get_args():
    parser = argparse.ArgumentParser("Database setup")
    parser.add_argument("--add-admin", action="store_true")
    return parser.parse_args()


def main():
    args = get_args()
    db.setup_database()
    if args.add_admin:
        salt = util.random_string()
        password = "password"
        db.insert_user(user.AdminUser(
            "admin", "admin", datetime.datetime.now(), util.get_hash(salt + password), salt, None, None
        ))


if __name__ == '__main__':
    main()
