import os
import json
import streamlit as st

# -----------------------------------------
# CHAT DIRECTORY
# -----------------------------------------


def get_chat_dir():
    user = st.session_state.get("user")
    path = f"users/{user}/chats"
    os.makedirs(path, exist_ok=True)
    return path


# -----------------------------------------
# LIST CHATS
# -----------------------------------------


def list_chats():
    chat_dir = get_chat_dir()
    files = os.listdir(chat_dir)
    return [
        f.replace(".json", "")
        for f in files
        if f.endswith(".json")
    ]


# -----------------------------------------
# LOAD CHAT
# -----------------------------------------


def load_chat(chat_name):
    path = f"{get_chat_dir()}/{chat_name}.json"

    if os.path.exists(path):
        try:
            with open(path, "r") as f:
                return json.load(f)
        except Exception:
            return []


# -----------------------------------------
# SAVE CHAT
# -----------------------------------------

def sanitize_chat_name(name):
    return "".join(c for c in name if c.isalnum() or c in ("_", "-"))

def save_chat(chat_name, messages):
    safe_name = sanitize_chat_name(chat_name)
    path = f"{get_chat_dir()}/{safe_name}.json"

    with open(path, "w") as f:
        json.dump(messages, f, indent=2)
