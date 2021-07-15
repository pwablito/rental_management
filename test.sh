#!/bin/bash

trap "kill -TERM 0" SIGINT SIGTERM EXIT

./setup_db.sh

cd api

# Run database and service tests

echo "Running database tests"

./test.py

echo "Psssed all database tests"

echo "Running test server"


./app.py > /dev/null 2>&1 &

# Wait for the server to start
sleep 1

# Run REST tests

function test_endpoint {
    # $1 is endpoint name, $2 is json string, $3 is content that should be in tht result
    echo "Testing $1"
    output=`curl -X POST -H "Content-Type: application/json" -d "$2" http://127.0.0.1:5000/$1 2>/dev/null`
    if [ -z "$(echo $output | grep "$3")" ]; then
        echo "Failed"
        echo "Output: $output"
        exit 1
    fi
}

test_endpoint "/api/login" '{"username":"admin","password":"password"}' "\"success\": true"
test_endpoint "/api/login" '{"username":"admin","password":"incorrect"}' "\"success\": false"
test_endpoint "/api/login" '{"username":"admin"}' "Missing fields"
test_endpoint "/api/register" '{"username":"test","password":"test"}' "Missing fields"
test_endpoint "/api/register" '{"username":"test","password":"test","name":"test"}' "\"success\": true"
test_endpoint "/api/register" '{"username":"test","password":"test","name":"test"}' "\"success\": false"

admin_token=`curl -X POST -H "Content-Type: application/json" -d '{"username":"admin","password":"password"}' http://127.0.0.1:5000/api/login 2>/dev/null | python3 -c "import sys, json; print(json.load(sys.stdin)['token'])"`

test_endpoint "/api/create_user" "{}" "Missing fields"
test_endpoint "/api/create_user" "{\"username\":\"client\",\"password\":\"test\",\"name\":\"Client\",\"type\":\"client\",\"token\":\"$admin_token\"}" "\"success\": true"
test_endpoint "/api/create_user" "{\"username\":\"realtor\",\"password\":\"test\",\"name\":\"Realtor\",\"type\":\"realtor\",\"token\":\"$admin_token\"}" "\"success\": true"

client_token=`curl -X POST -H "Content-Type: application/json" -d '{"username":"client","password":"test"}' http://127.0.0.1:5000/api/login 2>/dev/null | python3 -c "import sys, json; print(json.load(sys.stdin)['token'])"`
realtor_token=`curl -X POST -H "Content-Type: application/json" -d '{"username":"realtor","password":"test"}' http://127.0.0.1:5000/api/login 2>/dev/null | python3 -c "import sys, json; print(json.load(sys.stdin)['token'])"`

# Client and Realtor can not create a user
test_endpoint "/api/create_user" "{\"username\":\"user\",\"password\":\"test\",\"name\":\"user\",\"type\":\"realtor\",\"token\":\"$realtor_token\"}" "\"success\": false"
test_endpoint "/api/create_user" "{\"username\":\"user\",\"password\":\"test\",\"name\":\"user\",\"type\":\"realtor\",\"token\":\"$client_token\"}" "\"success\": false"
# User already exists
test_endpoint "/api/create_user" "{\"username\":\"realtor\",\"password\":\"test\",\"name\":\"Realtor\",\"type\":\"realtor\",\"token\":\"$admin_token\"}" "\"success\": false"

test_endpoint "/api/create_listing" "{}" "Missing fields"
# Admin and realtor can create a listing
test_endpoint "/api/create_listing" "{\"name\":\"listing\",\"description\":\"a listing\",\"floor_area\":1000,\"price\":1000,\"rooms\":2,\"bathrooms\":1,\"is_listed\":true,\"latitude\":0,\"longitude\":0,\"realtor\":\"realtor\",\"token\":\"$admin_token\"}" "\"success\": true"
test_endpoint "/api/create_listing" "{\"name\":\"listing\",\"description\":\"a listing\",\"floor_area\":1000,\"price\":1000,\"rooms\":2,\"bathrooms\":1,\"is_listed\":true,\"latitude\":0,\"longitude\":0,\"realtor\":\"realtor\",\"token\":\"$realtor_token\"}" "\"success\": true"
# Client can not create a listing
test_endpoint "/api/create_listing" "{\"name\":\"listing\",\"description\":\"a listing\",\"floor_area\":1000,\"price\":1000,\"rooms\":2,\"bathrooms\":1,\"is_listed\":true,\"latitude\":0,\"longitude\":0,\"realtor\":\"realtor\",\"token\":\"$client_token\"}" "\"success\": false"

test_endpoint "/api/get_users" "{}" "Missing fields"
# Only admin can get user information
test_endpoint "/api/get_users" "{\"token\":\"$admin_token\"}" "\"success\": true"
test_endpoint "/api/get_users" "{\"token\":\"$realtor_token\"}" "\"success\": false"
test_endpoint "/api/get_users" "{\"token\":\"$client_token\"}" "\"success\": false"

test_endpoint "/api/get_listings" "{}" "Missing fields"
# Every user can get listings
test_endpoint "/api/get_listings" "{\"token\":\"$admin_token\"}" "\"success\": true"
test_endpoint "/api/get_listings" "{\"token\":\"$realtor_token\"}" "\"success\": true"
test_endpoint "/api/get_listings" "{\"token\":\"$client_token\"}" "\"success\": true"

listing_id=`curl -X POST -H "Content-Type: application/json" -d "{\"token\":\"$client_token\"}" http://127.0.0.1:5000/api/get_listings 2>/dev/null | python3 -c "import sys, json; print(json.load(sys.stdin)['listings'][0]['id'])"`

test_endpoint "/api/update_listing" "{}" "Missing fields"
# Clients can not update listings
test_endpoint "/api/update_listing" "{\"listing\": {\"id\":\"$listing_id\",\"name\":\"new_name_1\",\"description\":\"a listing\",\"floor_area\":1000,\"price\":1000,\"rooms\":2,\"bathrooms\":1,\"is_listed\":true,\"latitude\":0,\"longitude\":0,\"realtor\":\"realtor\"},\"token\":\"$admin_token\"}" "\"success\": true"
test_endpoint "/api/update_listing" "{\"listing\": {\"id\":\"$listing_id\",\"name\":\"new_name_2\",\"description\":\"a listing\",\"floor_area\":1000,\"price\":1000,\"rooms\":2,\"bathrooms\":1,\"is_listed\":true,\"latitude\":0,\"longitude\":0,\"realtor\":\"realtor\"},\"token\":\"$realtor_token\"}" "\"success\": true"
test_endpoint "/api/update_listing" "{\"listing\": {\"id\":\"$listing_id\",\"name\":\"new_name_3\",\"description\":\"a listing\",\"floor_area\":1000,\"price\":1000,\"rooms\":2,\"bathrooms\":1,\"is_listed\":true,\"latitude\":0,\"longitude\":0,\"realtor\":\"realtor\"},\"token\":\"$client_token\"}" "\"success\": false"

test_endpoint "/api/update_user" "{}" "Missing fields"

echo "Passed all API tests"
