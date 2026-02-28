import sqlite3

DB_PATH = "healthcoach.db"

def get_connection():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.execute("""
    CREATE TABLE IF NOT EXISTS users (
        username TEXT PRIMARY KEY,
        password TEXT
    )
    """)
    conn.execute("""
    CREATE TABLE IF NOT EXISTS memory (
        username TEXT PRIMARY KEY,
        data TEXT
    )
    """)
    conn.execute("""
    CREATE TABLE IF NOT EXISTS chats (
        chat_id TEXT PRIMARY KEY,
        username TEXT,
        data TEXT
    )
    """)
    conn.commit()
    return conn