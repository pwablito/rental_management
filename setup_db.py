#!/usr/bin/env python3

import sqlite3
from api import db


if __name__ == '__main__':
    db.setup_database()
