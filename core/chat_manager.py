import json
import streamlit as st
from core.database import get_connection


def list_chats():
    username = st.session_state.get("user")
    if not username:
        return []

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT chat_id FROM chats WHERE username=? ORDER BY rowid DESC",
        (username,)
    )

    rows = cursor.fetchall()
    return [r[0] for r in rows]


def load_chat(chat_id):
    if not chat_id:
        return []

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT data FROM chats WHERE chat_id=?",
        (chat_id,)
    )

    row = cursor.fetchone()

    if row:
        return json.loads(row[0])

    return []


def save_chat(chat_id, messages):
    username = st.session_state.get("user")
    if not username:
        return

    conn = get_connection()
    cursor = conn.cursor()

    data = json.dumps(messages)

    cursor.execute("""
        INSERT INTO chats (chat_id, username, data)
        VALUES (?, ?, ?)
        ON CONFLICT(chat_id)
        DO UPDATE SET data=excluded.data
    """, (chat_id, username, data))

    conn.commit()