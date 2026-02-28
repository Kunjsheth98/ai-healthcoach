import hashlib
from core.database import get_connection

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def register_user(username, password):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT username FROM users WHERE username=?", (username,))
    if cursor.fetchone():
        return False, "Username already exists."

    cursor.execute(
        "INSERT INTO users (username, password) VALUES (?, ?)",
        (username, hash_password(password))
    )
    conn.commit()
    return True, "Registration successful!"

def login_user(username, password):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT password FROM users WHERE username=?",
        (username,)
    )
    row = cursor.fetchone()

    if row and row[0] == hash_password(password):
        return True
    return False