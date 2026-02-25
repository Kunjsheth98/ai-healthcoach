# =====================================================
# 🧠 IDENTITY ENGINE
# Turns habits into personal identity
# =====================================================

import streamlit as st

# -----------------------------------
# DETERMINE USER IDENTITY
# -----------------------------------


def compute_identity(memory):

    streak = memory.get("streak_days", 0)
    health_score = memory.get("health_score", 50)
    exercise = memory.get("exercise_done", False)

    identity = "Explorer"
    message = "You have started your health journey."

    if streak >= 30:
        identity = "Elite Self-Manager"
        message = "Health is now part of who you are."

    elif streak >= 14:
        identity = "Health Performer"
        message = "You are actively managing your health."

    elif streak >= 7:
        identity = "Discipline Creator"
        message = "Your routine is becoming a real lifestyle."

    elif streak >= 3:
        identity = "Consistency Builder"
        message = "You are building consistency — small wins daily."

    # bonus reinforcement
    if health_score > 75 and exercise:
        message += " Your actions show strong commitment."

    memory["identity_level"] = identity
    memory["identity_message"] = message


# -----------------------------------
# UI DISPLAY
# -----------------------------------


def identity_engine_ui(memory):

    compute_identity(memory)

    identity = memory.get("identity_level", "Explorer")
    msg = memory.get("identity_message", "")

    st.subheader("🧠 Your Health Identity")

    st.success(f"Identity Level: **{identity}**")
    st.info(msg)
