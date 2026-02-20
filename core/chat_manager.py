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
    return [f.replace(".json", "") for f in files]


# -----------------------------------------
# LOAD CHAT
# -----------------------------------------


def load_chat(chat_name):
    path = f"{get_chat_dir()}/{chat_name}.json"

    if os.path.exists(path):
        with open(path, "r") as f:
            return json.load(f)

    return []


# -----------------------------------------
# SAVE CHAT
# -----------------------------------------


def save_chat(chat_name, messages):
    path = f"{get_chat_dir()}/{chat_name}.json"

    with open(path, "w") as f:
        json.dump(messages, f, indent=2)
