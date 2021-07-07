#!/bin/bash

cd api
rm db.sqlite 2> /dev/null
./setup_db.py
