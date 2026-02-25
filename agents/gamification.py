import streamlit as st
from datetime import datetime, timedelta
from core.memory import save_memory

# --------------------------------------------------
# UPDATE STREAK
# --------------------------------------------------


def update_streak(memory):

    today = datetime.now().date().isoformat()
    last = memory.get("last_checkin_date")

    if last == today:
        return

    if last:
        yesterday = (datetime.now().date() - timedelta(days=1)).isoformat()

        if last == yesterday:
            memory["streak_days"] += 1
        else:
            memory["streak_days"] = 1
    else:
        memory["streak_days"] = 1

    memory["last_checkin_date"] = today
    save_memory(memory)


# --------------------------------------------------
# XP SYSTEM
# --------------------------------------------------


def add_xp(memory):

    xp_gain = 10

    if memory["exercise_done"]:
        xp_gain += 10

    if memory["water_intake"] >= 5:
        xp_gain += 5

    if memory["sleep_hours"] >= 7:
        xp_gain += 5

    memory.setdefault("xp_points", 0)
    memory["xp_points"] += xp_gain

    update_level(memory)

    save_memory(memory)


# --------------------------------------------------
# LEVEL SYSTEM
# --------------------------------------------------


def update_level(memory):

    xp = memory["xp_points"]

    level = min(10, xp // 50 + 1)
    memory["health_level"] = level


# --------------------------------------------------
# UI DISPLAY
# --------------------------------------------------


def gamification_ui(memory):

    st.subheader("🏆 Health Progress")

    col1, col2, col3 = st.columns(3)

    col1.metric("🔥 Streak", f"{memory.get('streak_days',0)} days")
    col2.metric("⭐ XP", memory.get("xp_points",0))
    col3.metric("🏅 Level", memory.get("health_level",1))

    if memory["streak_days"] >= 5:
        st.success("Amazing consistency! Keep going 🔥")
