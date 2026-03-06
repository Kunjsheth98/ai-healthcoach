import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
os.makedirs(DATA_DIR, exist_ok=True)
DB_PATH = os.path.join(DATA_DIR, "healthcoach.db")

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