from datetime import datetime, timedelta
import streamlit as st
from core.memory import save_memory

# ---------------------------------------------
# LIMIT CONFIG
# ---------------------------------------------

FREE_DAILY_LIMIT = 40
PREMIUM_DAILY_LIMIT = 300

FREE_COOLDOWN = 5  # seconds
PREMIUM_COOLDOWN = 1


# ---------------------------------------------
# INITIALIZE TRACKING
# ---------------------------------------------


def init_usage(memory):

    if "usage" not in memory:
        memory["usage"] = {
            "daily_count": 0,
            "last_reset": datetime.now().date().isoformat(),
            "last_message_time": "",
        }


# ---------------------------------------------
# RESET DAILY COUNTER
# ---------------------------------------------


def reset_if_new_day(memory):

    today = datetime.now().date().isoformat()

    if memory["usage"]["last_reset"] != today:
        memory["usage"]["daily_count"] = 0
        memory["usage"]["last_reset"] = today


# ---------------------------------------------
# CHECK LIMITS
# ---------------------------------------------


def check_rate_limit(memory):

    init_usage(memory)
    reset_if_new_day(memory)

    user_plan = st.session_state.get("plan", "free")

    limit = PREMIUM_DAILY_LIMIT if user_plan == "premium" else FREE_DAILY_LIMIT
    cooldown = PREMIUM_COOLDOWN if user_plan == "premium" else FREE_COOLDOWN

    # Daily limit
    if memory["usage"]["daily_count"] >= limit:
        return False, "Daily AI usage limit reached. Try again tomorrow."

    # Cooldown check
    last_time = memory["usage"]["last_message_time"]

    if last_time:
        last = datetime.fromisoformat(last_time)
        if datetime.now() - last < timedelta(seconds=cooldown):
            return False, f"Please wait {cooldown} seconds before next message."

    return True, ""


# ---------------------------------------------
# REGISTER USAGE
# ---------------------------------------------


def register_usage(memory):

    memory["usage"]["daily_count"] += 1
    memory["usage"]["last_message_time"] = datetime.now().isoformat()

    save_memory(memory)
