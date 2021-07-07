import json
import datetime
from flask import request
import util
import user
import listing
import db
import error


def register():
    request_data = json.loads(request.data.decode('utf-8'))
    salt = util.random_string()
    password_hash = util.get_hash(salt + request_data["password"])
    try:
        token = util.random_string()
        entry = user.ClientUser(
            request_data["username"], request_data["name"], datetime.datetime.now(), password_hash, salt, token)
        db.insert_user(entry)
        return json.dumps({
            "success": True,
            "user": entry.to_dict(),
            "token": token,
        })
    except error.UserAlreadyExistsException:
        return json.dumps({
            "success": False,
            "message": "Username already taken",
        })


def login():
    request_data = json.loads(request.data.decode('utf-8'))
    try:
        entry = db.get_user(request_data["username"])
    except error.UserNotFoundException:
        return json.dumps({
            "success": False,
            "message": "Invalid username",
        })
    if util.get_hash(entry.password_salt + request_data["password"]) == entry.password_hash:
        token = util.random_string()
        db.update_token(entry.username, token)
        return json.dumps({
            "success": True,
            "user": entry.to_dict(),
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
    try:
        entry = db.get_user_by_token(request_data["token"])
        is_client = False
        if not entry:
            return json.dumps({
                "success": False,
                "message": "Invalid token",
            })
        if type(entry) == user.ClientUser:
            is_client = True
        return json.dumps({
            "success": True,
            "listings": [listing.to_dict() for listing in db.get_all_listings(only_listed=is_client)]
        })
    except Exception as e:
        raise e
        return json.dumps({
            "success": False,
            "message": "Something went wrong",
        })


def create_listing():
    try:
        request_data = json.loads(request.data.decode('utf-8'))
        listing_id = util.random_string(length=20)
        entry = db.get_user_by_token(request_data["token"])
        if not user:
            return json.dumps({
                "success": False,
                "message": "Invalid token",
            })
        if type(entry) == user.ClientUser:
            return json.dumps({
                "success": False,
                "message": "Client user can not create listings",
            })
        db.insert_listing(listing.Listing(
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
            True
        ))
        return json.dumps({
            "success": True,
        })
    except KeyError as e:
        return json.dumps({
            "success": False,
            "message": "Missing fields",
        })


def delete_listing():
    try:
        request_data = json.loads(request.data.decode('utf-8'))
        entry = db.get_user_by_token(request_data["token"])
        if not user:
            return json.dumps({
                "success": False,
                "message": "Invalid token",
            })
        if type(entry) == user.ClientUser:
            return json.dumps({
                "success": False,
                "message": "Client user can not delete listings",
            })
        db.delete_listing(request_data["id"])
        return json.dumps({
            "success": True,
        })
    except KeyError:
        return json.dumps({
            "success": False,
            "message": "Missing fields",
        })


def delete_user():
    try:
        request_data = json.loads(request.data.decode('utf-8'))
        entry = db.get_user_by_token(request_data["token"])
        if not entry:
            return json.dumps({
                "success": False,
                "message": "Invalid token",
            })
        if type(entry) != user.AdminUser:
            return json.dumps({
                "success": False,
                "message": "Only administrators can not delete users",
            })
        db.delete_user(request_data["username"])
        return json.dumps({
            "success": True,
        })
    except KeyError:
        return json.dumps({
            "success": False,
            "message": "Missing fields",
        })


def get_users():
    request_data = json.loads(request.data.decode('utf-8'))
    try:
        entry = db.get_user_by_token(request_data["token"])
        if not entry:
            return json.dumps({
                "success": False,
                "message": "Invalid token",
            })
        if type(entry) != user.AdminUser:
            return json.dumps({
                "success": False,
                "message": "Only administrators can view user data",
            })
        return json.dumps({
            "success": True,
            "users": [current_user.to_dict() for current_user in db.get_all_users()]
        })
    except Exception as e:
        raise e
        return json.dumps({
            "success": False,
            "message": "Something went wrong",
        })