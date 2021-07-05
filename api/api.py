import json
import datetime
from flask import request
import api.util
import api.user
import api.db


def register():
    request_data = json.loads(request.data.decode('utf-8'))
    salt = api.util.random_string()
    password_hash = api.util.get_hash(salt + request_data["password"])
    try:
        token = api.util.random_string()
        user = api.user.ClientUser(request_data["username"], request_data["name"], datetime.datetime.now(), password_hash, salt, token)
        api.db.insert_user(user)
        return json.dumps({
            "success": True,
            "user": user.to_dict(),
            "token": token,
        })
    except api.error.UserAlreadyExistsException:
        return json.dumps({
            "success": False,
            "message": "Username already taken",
        })

def login():
    request_data = json.loads(request.data.decode('utf-8'))
    try:
        user = api.db.get_user(request_data["username"])
    except api.error.UserNotFoundException:
        return json.dumps({
            "success": False,
            "message": "Invalid username",
        })
    if api.util.get_hash(user.password_salt + request_data["password"]) == user.password_hash:
        token = api.util.random_string()
        api.db.update_token(user.username, token)
        return json.dumps({
            "success": True,
            "user": user.to_dict(),
            "token": token,
        })
    return json.dumps({
        "success": False,
        "message": "Incorrect password",
    })

def update_user():
    request_data = json.loads(request.data.decode('utf-8'))
    return json.dumps({
        "success": False,
        "message": "Not implemented",
    })

def get_listings():
    request_data = json.loads(request.data.decode('utf-8'))
    return json.dumps({
        "success": False,
        "message": "Not implemented",
    })
