import json
import datetime
from flask import request
import util
import user
import listing
import db
import error


def register():
    try:
        request_data = json.loads(request.data.decode('utf-8'))
        salt = util.random_string()
        password_hash = util.get_hash(salt + request_data["password"])
        entry = user.ClientUser(
            request_data["username"], request_data["name"], datetime.datetime.now(), password_hash, salt, None, None)
        db.insert_user(entry)
        token = util.random_string()
        db.set_token(entry.username, token)
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
    except KeyError:
        return json.dumps({
            "success": False,
            "message": "Missing fields",
        })
    except Exception as e:
        return json.dumps({
            "success": False,
            "message": "Something went wrong",
        })


def login():
    try:
        request_data = json.loads(request.data.decode('utf-8'))
        entry = db.get_user(request_data["username"])
        if util.get_hash(entry.password_salt + request_data["password"]) == entry.password_hash:
            token = util.random_string()
            db.set_token(entry.username, token)
            return json.dumps({
                "success": True,
                "user": entry.to_dict(),
                "token": token,
            })
        return json.dumps({
            "success": False,
            "message": "Incorrect password",
        })
    except error.UserNotFoundException:
        return json.dumps({
            "success": False,
            "message": "Invalid username",
        })
    except KeyError:
        return json.dumps({
            "success": False,
            "message": "Missing fields",
        })
    except Exception as e:
        return json.dumps({
            "success": False,
            "message": "Something went wrong",
        })


def update_user():
    try:
        request_data = json.loads(request.data.decode('utf-8'))
        entry = db.get_user_by_token(request_data["token"])
        if util.token_is_expired(entry.token_created):
            return json.dumps({
                "success": False,
                "message": "Token expired"
            })
        if not entry:
            return json.dumps({
                "success": False,
                "message": "Invalid token",
            })
        if type(entry) != user.AdminUser:
            return json.dumps({
                "success": False,
                "message": "Only administrators can update users",
            })
        user_dict = request_data["user"]
        update_user = None
        if user_dict["type"] == "client":
            update_user = user.ClientUser(user_dict["username"], user_dict["name"], None, None, None, None, None)
        elif user_dict["type"] == "realtor":
            update_user = user.RealtorUser(user_dict["username"], user_dict["name"], None, None, None, None, None)
        elif user_dict["type"] == "admin":
            update_user = user.AdminUser(user_dict["username"], user_dict["name"], None, None, None, None, None)
        else:
            raise error.InvalidUserTypeException
        db.update_user(update_user)
        if "password" in request_data:
            password_salt = util.random_string()
            password_hash = util.get_hash(password_salt + request_data["password"])
            db.set_user_password(update_user.username, password_hash, password_salt)
        return json.dumps({
            "success": True,
        })
    except error.UserNotFoundException:
        return json.dumps({
            "success": False,
            "message": "Invalid token",
        })
    except KeyError as e:
        return json.dumps({
            "success": False,
            "message": "Missing fields",
        })
    except Exception as e:
        return json.dumps({
            "success": False,
            "message": "Something went wrong"
        })


def get_listings():
    try:
        request_data = json.loads(request.data.decode('utf-8'))
        entry = db.get_user_by_token(request_data["token"])
        if util.token_is_expired(entry.token_created):
            return json.dumps({
                "success": False,
                "message": "Token expired"
            })
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
    except error.UserNotFoundException:
        return json.dumps({
            "success": False,
            "message": "Invalid token",
        })
    except KeyError as e:
        return json.dumps({
            "success": False,
            "message": "Missing fields",
        })
    except Exception as e:
        return json.dumps({
            "success": False,
            "message": "Something went wrong",
        })


def create_listing():
    try:
        request_data = json.loads(request.data.decode('utf-8'))
        listing_id = util.random_string(length=20)
        entry = db.get_user_by_token(request_data["token"])
        if util.token_is_expired(entry.token_created):
            return json.dumps({
                "success": False,
                "message": "Token expired"
            })
        if not entry:
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
            request_data["is_listed"],
            request_data["realtor"],
        ))
        return json.dumps({
            "success": True,
        })
    except error.UserNotFoundException:
        return json.dumps({
            "success": False,
            "message": "Invalid token",
        })
    except KeyError as e:
        return json.dumps({
            "success": False,
            "message": "Missing fields",
        })
    except Exception as e:
        return json.dumps({
            "success": False,
            "message": "Something went wrong",
        })


def delete_listing():
    try:
        request_data = json.loads(request.data.decode('utf-8'))
        entry = db.get_user_by_token(request_data["token"])
        if util.token_is_expired(entry.token_created):
            return json.dumps({
                "success": False,
                "message": "Token expired"
            })
        if not entry:
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
    except error.UserNotFoundException:
        return json.dumps({
            "success": False,
            "message": "Invalid token",
        })
    except KeyError:
        return json.dumps({
            "success": False,
            "message": "Missing fields",
        })
    except Exception as e:
        return json.dumps({
            "success": False,
            "message": "Something went wrong",
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
        if util.token_is_expired(entry.token_created):
            return json.dumps({
                "success": False,
                "message": "Token expired"
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
    except error.UserNotFoundException:
        return json.dumps({
            "success": False,
            "message": "Invalid token",
        })
    except KeyError as e:
        return json.dumps({
            "success": False,
            "message": "Missing fields",
        })
    except Exception as e:
        return json.dumps({
            "success": False,
            "message": "Something went wrong",
        })


def get_users():
    try:
        request_data = json.loads(request.data.decode('utf-8'))
        entry = db.get_user_by_token(request_data["token"])
        if util.token_is_expired(entry.token_created):
            return json.dumps({
                "success": False,
                "message": "Token expired"
            })
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
    except error.UserNotFoundException:
        return json.dumps({
            "success": False,
            "message": "Invalid token",
        })
    except KeyError as e:
        return json.dumps({
            "success": False,
            "message": "Missing fields",
        })
    except Exception as e:
        return json.dumps({
            "success": False,
            "message": "Something went wrong",
        })

def create_user():
    try:
        request_data = json.loads(request.data.decode('utf-8'))
        entry = db.get_user_by_token(request_data["token"])
        if util.token_is_expired(entry.token_created):
            return json.dumps({
                "success": False,
                "message": "Token expired"
            })
        if not entry:
            return json.dumps({
                "success": False,
                "message": "Invalid token",
            })
        if type(entry) != user.AdminUser:
            return json.dumps({
                "success": False,
                "message": "Only administrators can create users",
            })
        salt = util.random_string()
        new_user = user.User(
            request_data["username"],
            request_data["name"],
            datetime.datetime.now(),
            util.get_hash(salt + request_data["password"]),
            salt,
            None,
            None,
        )
        if request_data["type"] == "client":
            new_user = new_user.to_client_user()
        if request_data["type"] == "realtor":
            new_user = new_user.to_realtor_user()
        if request_data["type"] == "admin":
            new_user = new_user.to_admin_user()
        db.insert_user(new_user)
        return json.dumps({
            "success": True,
        })
    except error.UserNotFoundException:
        return json.dumps({
            "success": False,
            "message": "Invalid token",
        })
    except KeyError as e:
        return json.dumps({
            "success": False,
            "message": "Missing fields",
        })
    except Exception as e:
        return json.dumps({
            "success": False,
            "message": "Something went wrong",
        })

def update_listing():
    try:
        request_data = json.loads(request.data.decode('utf-8'))
        entry = db.get_user_by_token(request_data["token"])
        if util.token_is_expired(entry.token_created):
            return json.dumps({
                "success": False,
                "message": "Token expired"
            })
        if not entry:
            return json.dumps({
                "success": False,
                "message": "Invalid token",
            })
        if type(entry) == user.ClientUser:
            return json.dumps({
                "success": False,
                "message": "Clients can not update listings",
            })
        listing_dict = request_data["listing"]
        try:
            db.get_listing_by_id(listing_dict["id"])
        except error.ListingNotFoundException:
            return json.dumps({
                "success": False,
                "message": "Listing not found",
            })
        db.update_listing(listing.Listing(
            listing_dict["id"],
            listing_dict["name"],
            listing_dict["description"],
            listing_dict["floor_area"],
            listing_dict["price"],
            listing_dict["rooms"],
            listing_dict["bathrooms"],
            None,
            listing_dict["latitude"],
            listing_dict["longitude"],
            listing_dict["is_listed"],
            listing_dict["realtor"],
        ))
        return json.dumps({
            "success": True,
        })
    except error.UserNotFoundException:
        return json.dumps({
            "success": False,
            "message": "Invalid token",
        })
    except KeyError as e:
        return json.dumps({
            "success": False,
            "message": "Missing fields",
        })
    except Exception as e:
        return json.dumps({
            "success": False,
            "message": "Something went wrong",
        })