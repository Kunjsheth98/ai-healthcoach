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

    try:
        with open(USERS_FILE, "r") as f:
            users = json.load(f)
    except Exception:
        users = {}

    if username not in users:
        return False

    stored = users[username]
    salt_hex, hash_hex = stored.split(":")

    salt = bytes.fromhex(salt_hex)
    new_hash = hashlib.pbkdf2_hmac(
        'sha256',
        password.encode(),
        salt,
        100000
    ).hex()

    if new_hash == hash_hex:
        return True

    return False
