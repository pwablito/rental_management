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
        user = api.user.ClientUser(
            request_data["username"], request_data["name"], datetime.datetime.now(), password_hash, salt, token)
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
    try:
        user = api.db.get_user_by_token(request_data["token"])
        is_client = False
        if not user:
            return json.dumps({
                "success": False,
                "message": "Invalid token",
            })
        if type(user) == api.user.ClientUser:
            is_client = True
        return json.dumps({
            "success": True,
            "listings": [listing.to_dict() for listing in api.db.get_all_listings(only_listed=is_client)]
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
        listing_id = api.util.random_string(length=20)
        user = api.db.get_user_by_token(request_data["token"])
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
        user = api.db.get_user_by_token(request_data["token"])
        if not user:
            return json.dumps({
                "success": False,
                "message": "Invalid token",
            })
        if type(user) == api.user.ClientUser:
            return json.dumps({
                "success": False,
                "message": "Client user can not delete listings",
            })
        api.db.delete_listing(request_data["id"])
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
        user = api.db.get_user_by_token(request_data["token"])
        if not user:
            return json.dumps({
                "success": False,
                "message": "Invalid token",
            })
        if type(user) != api.user.AdminUser:
            return json.dumps({
                "success": False,
                "message": "Only administrators can not delete users",
            })
        api.db.delete_user(request_data["username"])
        return json.dumps({
            "success": True,
        })
    except KeyError:
        return json.dumps({
            "success": False,
            "message": "Missing fields",
        })


def get_listings():
    request_data = json.loads(request.data.decode('utf-8'))
    try:
        user = api.db.get_user_by_token(request_data["token"])
        if not user:
            return json.dumps({
                "success": False,
                "message": "Invalid token",
            })
        if type(user) != api.user.AdminUser:
            return json.dumps({
                "success": False,
                "message": "Only administrators can view user data",
            })
        return json.dumps({
            "success": True,
            "users": [user.to_dict() for user in api.db.get_all_users()]
        })
    except Exception as e:
        raise e
        return json.dumps({
            "success": False,
            "message": "Something went wrong",
        })