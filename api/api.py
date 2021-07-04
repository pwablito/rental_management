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
        user = api.user.ClientUser(request_data["username"], request_data["name"], datetime.datetime.now(), password_hash, salt)
        api.db.insert_user(user)
        return json.dumps({
            "success": True,
            "user": user.to_dict(),
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
        # Success
        return json.dumps({
            "success": True,
            "user": user.to_dict(),
        })
    return json.dumps({
        "success": False,
        "message": "Incorrect password",
    })
