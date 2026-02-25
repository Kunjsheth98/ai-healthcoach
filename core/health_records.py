import os
import streamlit as st

# ----------------------------------------
# GET USER RECORD PATH
# ----------------------------------------


def get_records_path():

    user = st.session_state.get("user")

    if not user:
        return None

    path = f"users/{user}/records"
    os.makedirs(path, exist_ok=True)

    return path

# ----------------------------------------
# SAVE FILE
# ----------------------------------------
def sanitize_filename(name):
    return "".join(c for c in name if c.isalnum() or c in (".", "_", "-"))

def save_health_record(uploaded_file):

    path = get_records_path()
    if not path:
        return None

    safe_name = sanitize_filename(uploaded_file.name)
    file_path = os.path.join(path, safe_name)

    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    return file_path


# ----------------------------------------
# LIST RECORDS
# ----------------------------------------


def list_records():

    path = get_records_path()
    if not path:
        return []

    return [
        f for f in os.listdir(path)
        if os.path.isfile(os.path.join(path, f))
    ]
