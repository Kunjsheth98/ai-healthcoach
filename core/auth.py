import json
import os
import hashlib

USERS_FILE = "users/users.json"


# -------------------------------------
# CREATE USERS STORAGE
# -------------------------------------

def init_user_db():
    if not os.path.exists("users"):
        os.makedirs("users")

    if not os.path.exists(USERS_FILE):
        with open(USERS_FILE, "w") as f:
            json.dump({}, f)


# -------------------------------------
# PASSWORD HASHING
# -------------------------------------

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


# -------------------------------------
# REGISTER USER
# -------------------------------------

def register_user(username, password):

    init_user_db()

    with open(USERS_FILE, "r") as f:
        users = json.load(f)

    if username in users:
        return False, "User already exists"

    users[username] = hash_password(password)

    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=4)

    # create personal folder
    os.makedirs(f"users/{username}", exist_ok=True)

    return True, "User created successfully"


# -------------------------------------
# LOGIN USER
# -------------------------------------

def login_user(username, password):

    init_user_db()

    with open(USERS_FILE, "r") as f:
        users = json.load(f)

    if username not in users:
        return False

    if users[username] == hash_password(password):
        return True

    return False
