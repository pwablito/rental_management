import api.util

class User:
    def __init__(self, id, username, created_on, password_hash, password_salt):
        self.id = id
        self.username = username
        self.created_on = created_on
        self.password_hash = password_hash
        self.password_salt = password_salt

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.usename,
            "created_on": self.created_on,
        }

    def authenticate(self, password):
        return util.get_hash(password + self.password_salt) == self.password_hash


class ClientUser(User):
    def to_dict(self):
        return super().to_dict().update({
            "type": "client"
        })


class RealtorUser(User):
    def to_dict(self):
        return super().to_dict().update({
            "type": "realtor"
        })


class AdminUser(User):
    def to_dict(self):
        return super().to_dict().update({
            "type": "admin"
        })
