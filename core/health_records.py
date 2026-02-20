import os
import streamlit as st

# ----------------------------------------
# GET USER RECORD PATH
# ----------------------------------------


def get_records_path():

    user = st.session_state.get("user")

    path = f"users/{user}/records"
    os.makedirs(path, exist_ok=True)

    return path


# ----------------------------------------
# SAVE FILE
# ----------------------------------------


def save_health_record(uploaded_file):

    path = get_records_path()

    file_path = os.path.join(path, uploaded_file.name)

    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    return file_path


# ----------------------------------------
# LIST RECORDS
# ----------------------------------------


def list_records():

    path = get_records_path()

    return os.listdir(path)
