#!/bin/bash

trap "kill -TERM 0" SIGINT SIGTERM EXIT

# Run database and service tests

echo "Running service and database tests"

api/test.py

echo "Running test server"

api/app.py > /dev/null 2>&1 &

# Wait for the server to start
sleep 1

# Run REST tests

function test_endpoint {
    # $1 is endpoint name, $2 is json string, $3 is content that should be in tht result
    echo "Testing $1"
    output=`curl -X POST -H "Content-Type: application/json" -d "$2" http://127.0.0.1:5000/$1 2>/dev/null`
    if [ -z "$output" ]; then
        echo "Failed"
        echo "Output: $output"
        exit 1
    else
        echo "Passed"
    fi
}

test_endpoint "/api/login" '{"username":"admin","password":"test"}' "\"success\": true"
test_endpoint "/api/login" '{"username":"admin","password":"incorrect"}' "\"success\": false"
test_endpoint "/api/login" '{"username":"admin"}' "Missing fields"
test_endpoint "/api/register" '{"username":"test","password":"test"}' "Missing fields"
test_endpoint "/api/register" '{"username":"test","password":"test","name":"test"}' "\"success\": true"
test_endpoint "/api/register" '{"username":"test","password":"test","name":"test"}' "\"success\": false"

echo "Passed all API tests"
