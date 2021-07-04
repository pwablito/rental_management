import api.util

class User:
    def __init__(self, username, name, created_on, password_hash, password_salt):
        self.username = username
        self.name = name
        self.created_on = created_on
        self.password_hash = password_hash
        self.password_salt = password_salt

    def to_dict(self):
        return {
            "username": self.username,
            "name": self.name,
            "created_on": self.created_on.isoformat(),
        }

    def authenticate(self, password):
        return util.get_hash(password + self.password_salt) == self.password_hash


class ClientUser(User):
    def to_dict(self):
        user_data = super().to_dict()
        user_data.update({
            "type": "client"
        })
        return user_data

class RealtorUser(User):
    def to_dict(self):
        user_data = super().to_dict()
        user_data.update({
            "type": "realtor"
        })
        return user_data


class AdminUser(User):
    def to_dict(self):
        user_data = super().to_dict()
        user_data.update({
            "type": "admin"
        })
        return user_data
