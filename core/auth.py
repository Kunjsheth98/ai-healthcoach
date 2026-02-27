import json
import os
import hashlib

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
USERS_FILE = os.path.join(BASE_DIR, "users", "users.json")


# -------------------------------------
# CREATE USERS STORAGE
# -------------------------------------


def init_user_db():
    if not os.path.exists(os.path.join(BASE_DIR, "users")):
        os.makedirs(os.path.join(BASE_DIR, "users"))

    if not os.path.exists(USERS_FILE):
        with open(USERS_FILE, "w") as f:
            json.dump({}, f)


# -------------------------------------
# PASSWORD HASHING
# -------------------------------------


def hash_password(password, salt=None):

    if salt is None:
        salt = os.urandom(16)

    hashed = hashlib.pbkdf2_hmac(
        'sha256',
        password.encode(),
        salt,
        100000
    )

    return salt.hex() + ":" + hashed.hex()


# -------------------------------------
# REGISTER USER
# -------------------------------------


def register_user(username, password):
    init_user_db()

    with open(USERS_FILE, "r") as f:
        users = json.load(f)

    if username in users:
        return False, "User already exists."

    hashed = hashlib.sha256(password.encode()).hexdigest()
    users[username] = hashed

    with open(USERS_FILE, "w") as f:
        json.dump(users, f)

    return True, "User registered successfully!"


# -------------------------------------
# LOGIN USER
# -------------------------------------

def login_user(username, password):
    init_user_db()

    with open(USERS_FILE, "r") as f:
        users = json.load(f)

    hashed = hashlib.sha256(password.encode()).hexdigest()

    if username in users and users[username] == hashed:
        return True

    return False
