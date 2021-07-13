import random
import string
import hashlib
import datetime

def random_string(length=12):
    return ''.join(random.choice(string.ascii_uppercase + string.digits + string.ascii_lowercase) for _ in range(length))

def get_hash(text):
    return hashlib.sha256((text).encode()).hexdigest()

def token_is_expired(created_on):
    return datetime.datetime.now() > created_on + datetime.timedelta(hours=6)
