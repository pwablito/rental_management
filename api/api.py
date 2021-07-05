import json
import datetime
from flask import request
import api.util
import api.user
import api.listing
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
    try:
        return json.dumps({
            "success": True,
            "listings": [listing.to_dict() for listing in api.db.get_all_listings()]
        })
    except Exception as e:
        print(e)
        return json.dumps({
            "success": False,
            "message": "Something went wrong",
        })

def create_listing():
    request_data = json.loads(request.data.decode('utf-8'))
    user = api.db.get_user_by_token(request_data["token"])
    listing_id = api.util.random_string(length=20)
    if not user:
        return json.dumps({
            "success": False,
            "message": "Invalid token",
        })
    if type(user) == api.user.ClientUser:
        return json.dumps({
            "success": False,
            "message": "Client user can not create listings",
        })
    # All other user types are allowed to create listings
    try:
        api.db.insert_listing(api.listing.Listing(
            listing_id,
            request_data["name"],
            request_data["description"],
            request_data["floor_area"],
            request_data["price"],
            request_data["rooms"],
            request_data["bathrooms"],
            datetime.datetime.now(),
            request_data["latitude"],
            request_data["longitude"],
        ))
        return json.dumps({
            "success": True,
        })
    except KeyError as e:
        return json.dumps({
            "success": False,
            "message": "Missing fields",
        })
