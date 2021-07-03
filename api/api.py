import json
from flask import request
import util
import user


def register():
    request_data = json.loads(request.data.decode('utf-8'))
    salt = util.random_string()
    password_salt = util.get_hash(salt + request_data["password"])
    # TODO Insert to database, then continue
    return json.dumps({
        "success": False,
        "message": "Endpoint not implemented",
    })
