#!/bin/bash

cd client
npm run serve &
cd ..

cd api
./app.py
