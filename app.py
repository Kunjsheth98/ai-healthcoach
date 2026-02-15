import streamlit as st

# ================= AUTH =================
from core.auth import register_user, login_user

# ================= MEMORY =================
from core.memory import load_memory, save_memory

# ================= CHAT =================
from core.chat_manager import list_chats, load_chat, save_chat

# ================= SUBSCRIPTION =================
from core.subscription import has_premium_access, premium_lock

# ================= COST METER =================
from core.cost_meter import get_cost_summary

# ================= AGENTS =================
from agents.health_score import calculate_health_score
from agents.gamification import update_streak, add_xp, gamification_ui
from agents.morning_briefing import morning_briefing_ui
from agents.master_brain import health_master_brain

from agents.weekly_story import weekly_story_ui
from agents.adaptive_planner import adaptive_life_planner
from agents.planner import autonomous_planner_agent
from agents.movement_coach import movement_coach_agent

from agents.habit_brain import habit_insight_ui
from agents.emotion_engine import emotional_feedback_ui
from agents.personality_engine import personality_display_ui
from agents.health_twin import health_twin_ui
from agents.learning_engine import learning_engine_ui

from agents.health_vault import health_record_vault
from agents.prescription_reader import prescription_reader_ui

# ================= ADMIN =================
from admin.admin_dashboard import admin_dashboard

# ================= AI =================
from ai.coach import ask_health_coach

# ================= DASHBOARD =================
from dashboard.charts import show_health_chart


# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="AI HealthCoach",
    page_icon="🩺",
    layout="wide"
)

# =====================================================
# LOGIN SYSTEM
# =====================================================

if "user" not in st.session_state:
    st.session_state.user = None

if st.session_state.user is None:

    st.title("🔐 AI HealthCoach Login")

    tab1, tab2 = st.tabs(["Login", "Register"])

    with tab1:
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("Login"):
            if login_user(username, password):
                st.session_state.user = username
                st.session_state.plan = "free"
                st.rerun()
            else:
                st.error("Invalid credentials")

    with tab2:
        new_user = st.text_input("New Username")
        new_pass = st.text_input("New Password", type="password")

        if st.button("Register"):
            success, msg = register_user(new_user, new_pass)
            if success:
                st.success(msg)
            else:
                st.error(msg)

    st.stop()

# =====================================================
# LOAD MEMORY
# =====================================================

memory = load_memory()

st.title("🩺 AI HealthCoach")
st.caption(f"Logged in as: {st.session_state.user}")

# =====================================================
# ADMIN CONTROL
# =====================================================

ADMIN_USERS = ["demo"]  # change later

tabs = ["🏠 Dashboard", "💬 Coach", "📊 Insights", "🧭 Planner", "🗂️ Records"]

if st.session_state.user in ADMIN_USERS:
    tabs.append("🛠️ Admin")

all_tabs = st.tabs(tabs)

tab_dashboard = all_tabs[0]
tab_chat = all_tabs[1]
tab_insights = all_tabs[2]
tab_planner = all_tabs[3]
tab_records = all_tabs[4]

if st.session_state.user in ADMIN_USERS:
    tab_admin = all_tabs[5]

# =====================================================
# DASHBOARD TAB
# =====================================================

with tab_dashboard:

    st.subheader("📱 WhatsApp Notifications")

    phone = st.text_input(
        "Enter WhatsApp number",
        value=memory.get("phone_number", "")
    )

    if st.button("Save Number"):
        memory["phone_number"] = phone
        st.success("Number saved!")

    st.divider()

    st.subheader("Today's Overview")

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Health Score", memory["health_score"])
    c2.metric("Water", memory["water_intake"])
    c3.metric("Energy", memory["energy_level"])
    c4.metric("Sleep", memory["sleep_hours"])

    gamification_ui(memory)
    morning_briefing_ui(memory)

    # ================= COST METER =================
    requests, usd, inr = get_cost_summary(memory)

    st.divider()
    st.subheader("💰 AI Usage Today")

    cc1, cc2, cc3 = st.columns(3)
    cc1.metric("Requests Used", requests)
    cc2.metric("USD Spent", f"${usd}")
    cc3.metric("Estimated Cost", f"₹{inr}")

    st.divider()

    st.subheader("Daily Check-In")

    sleep = st.slider("Sleep Hours", 0, 12, memory["sleep_hours"])
    energy = st.slider("Energy", 1, 10, memory["energy_level"])
    exercise = st.checkbox("Exercise done", memory["exercise_done"])
    water = st.number_input("Water glasses", 0, 20, memory["water_intake"])

    if st.button("Save Check-In"):
        memory["sleep_hours"] = sleep
        memory["energy_level"] = energy
        memory["exercise_done"] = exercise
        memory["water_intake"] = water

        calculate_health_score(memory)
        update_streak(memory)
        add_xp(memory)

        st.success("Check-in saved!")

    st.divider()

    # 🧠 MASTER AI OPERATING SYSTEM
    health_master_brain(memory)

# =====================================================
# CHAT TAB
# =====================================================

with tab_chat:

    chats = list_chats()

    chat_name = st.selectbox(
        "Select Chat",
        chats if chats else ["default"]
    )

    new_chat = st.text_input("Create new chat")

    if st.button("Create Chat") and new_chat:
        save_chat(new_chat, [])
        st.rerun()

    messages = load_chat(chat_name)

    for m in messages:
        st.chat_message(m["role"]).write(m["content"])

    user_msg = st.chat_input("Ask your coach...")

    if user_msg:
        messages.append({"role": "user", "content": user_msg})

        reply = ask_health_coach(memory, user_msg, messages)

        messages.append({"role": "assistant", "content": reply})

        save_chat(chat_name, messages)
        st.rerun()

# =====================================================
# INSIGHTS TAB
# =====================================================

with tab_insights:

    show_health_chart(memory)

    habit_insight_ui(memory)
    emotional_feedback_ui(memory)
    personality_display_ui(memory)

    learning_engine_ui(memory)

    if has_premium_access("weekly_story"):
        weekly_story_ui(memory)
        health_twin_ui(memory)
    else:
        premium_lock()

# =====================================================
# PLANNER TAB
# =====================================================

with tab_planner:

    autonomous_planner_agent(memory)

    if has_premium_access("adaptive_planner"):
        adaptive_life_planner(memory)
    else:
        premium_lock()

    st.divider()

    if has_premium_access("movement_coach"):
        movement_coach_agent(memory)
    else:
        premium_lock()

# =====================================================
# RECORDS TAB
# =====================================================

with tab_records:
    health_record_vault()
    st.divider()
    prescription_reader_ui(memory)

# =====================================================
# ADMIN TAB
# =====================================================

if st.session_state.user in ADMIN_USERS:
    with tab_admin:
        admin_dashboard()

# =====================================================
# SAVE MEMORY
# =====================================================

save_memory(memory)
