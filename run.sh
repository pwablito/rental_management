#!/bin/bash

trap "kill -TERM 0" SIGINT SIGTERM EXIT

cd client
npm run serve &
cd ..

cd api
./app.py
