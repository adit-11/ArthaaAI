import hashlib

# In-memory user store (for now)
users_db = {}

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def register_user(username, password):
    if username in users_db:
        return False
    users_db[username] = hash_password(password)
    return True

def authenticate_user(username, password):
    if username not in users_db:
        return False
    return users_db[username] == hash_password(password)