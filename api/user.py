import util

class User:
    def __init__(self, username, name, created_on, password_hash, password_salt, token, token_created):
        self.username = username
        self.name = name
        self.created_on = created_on
        self.password_hash = password_hash
        self.password_salt = password_salt
        self.token = token
        self.token_created = token_created

    def to_dict(self):
        return {
            "username": self.username,
            "name": self.name,
            "created_on": self.created_on.isoformat(),
        }

    def authenticate(self, password):
        return util.get_hash(password + self.password_salt) == self.password_hash

    def to_client_user(self):
        return ClientUser(self.username, self.name, self.created_on,  self.password_hash, self.password_salt, self.token, self.token_created)

    def to_realtor_user(self):
        return RealtorUser(self.username, self.name, self.created_on,  self.password_hash, self.password_salt, self.token, self.token_created)

    def to_admin_user(self):
        return AdminUser(self.username, self.name, self.created_on,  self.password_hash, self.password_salt, self.token, self.token_created)

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
