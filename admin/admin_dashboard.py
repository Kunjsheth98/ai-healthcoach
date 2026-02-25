import os
import json
import streamlit as st

# --------------------------------------------------
# GET ALL USERS
# --------------------------------------------------


def get_all_users():

    if not os.path.exists("users"):
        return []

    return [
        name
        for name in os.listdir("users")
        if os.path.isdir(os.path.join("users", name))
    ]


# --------------------------------------------------
# LOAD USER MEMORY
# --------------------------------------------------


def load_user_memory(user):

    path = f"users/{user}/memory.json"

    if not os.path.exists(path):
        return None

    try:
        with open(path, "r") as f:
            return json.load(f)
    except Exception:
        return None


# --------------------------------------------------
# ADMIN DASHBOARD UI
# --------------------------------------------------


def admin_dashboard():

    st.title("🛠️ AI Admin & Monitoring Dashboard")

    users = get_all_users()

    st.subheader("👥 User Overview")
    st.metric("Total Users", len(users))

    if not users:
        st.info("No users yet.")
        return

    selected_user = st.selectbox("Select User", users)

    memory = load_user_memory(selected_user)

    if not memory:
        st.warning("No memory found.")
        return

    st.divider()

    # ---------------- HEALTH STATUS ----------------
    st.subheader("🩺 Health Status")

    col1, col2, col3 = st.columns(3)

    col1.metric("Health Score", memory.get("health_score", 0))
    col2.metric("Streak", memory.get("streak_days", 0))
    col3.metric("Level", memory.get("health_level", 1))

    # ---------------- MASTER BRAIN LOGS ------------
    st.subheader("🧠 Master Brain Decisions")

    logs = memory.get("master_decision_log", [])
    if not isinstance(logs, list):
        logs = []

    if logs:
        for log in reversed(logs[-10:]):
            st.write(log)
    else:
        st.info("No decisions logged yet.")

    # ---------------- AUTONOMOUS COACH LOG ---------
    st.subheader("🤖 Autonomous Coach Messages")

    coach_logs = memory.get("auto_coach_log", [])
    if not isinstance(coach_logs, list):
        coach_logs = []

    if coach_logs:
        for msg in reversed(coach_logs[-10:]):
            st.write(msg)
    else:
        st.info("No coaching messages yet.")

    # ---------------- RISK HISTORY -----------------
    st.subheader("⚠️ Risk Predictions")

    risks = memory.get("risk_history", [])
    if not isinstance(risks, list):
        risks = []

    if risks:
        for r in reversed(risks[-10:]):
            st.error(r)
    else:
        st.info("No risks detected.")

    # ---------------- LEARNING ENGINE --------------
    st.subheader("🧠 Long-Term Learning Summary")

    summary = memory.get("long_term_summary", "")

    if summary:
        st.info(summary)
    else:
        st.info("Learning engine not updated yet.")
