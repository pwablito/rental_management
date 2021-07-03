import random
import string
import hashlib

def random_string(length=12):
    return ''.join(random.choice(string.ascii_uppercase + string.digits + string.ascii_lowercase) for _ in range(length))

def get_hash(text):
    return hashlib.sha256((text).encode()).hexdigest()
