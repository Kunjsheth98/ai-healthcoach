import streamlit as st

# ================= AUTH =================
from core.auth import register_user, login_user

# ================= MEMORY =================
from core.memory import load_memory, save_memory

# ================= CHAT =================
from core.chat_manager import list_chats, load_chat, save_chat

# ================= SUBSCRIPTION =================
from core.subscription import has_premium_access, premium_lock

# ================= COST =================
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
from agents.emotional_rewards import emotional_reward_engine
from agents.identity_engine import identity_engine_ui


# NEW INTELLIGENCE LAYERS
from agents.nutritionist_brain import nutritionist_brain
from agents.metabolic_predictor import metabolic_predictor
from agents.behavior_brain import behavior_brain

# ================= ADMIN =================
from admin.admin_dashboard import admin_dashboard
from admin.control_center import admin_control_center

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
# ADMIN USERS
# =====================================================

ADMIN_USERS = ["demo"]

tabs = ["🏠 Dashboard", "💬 Coach", "📊 Insights", "🧭 Planner", "🗂️ Records"]

if st.session_state.user in ADMIN_USERS:
    tabs.append("🛠️ Admin")

all_tabs = st.tabs(tabs)

tab_dashboard, tab_chat, tab_insights, tab_planner, tab_records = all_tabs[:5]

if st.session_state.user in ADMIN_USERS:
    tab_admin = all_tabs[5]

# =====================================================
# DASHBOARD
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

    # ---------------- OVERVIEW ----------------
    st.subheader("Today's Overview")

    c1, c2, c3, c4, c5 = st.columns(5)

    c1.metric("🧠 Health Score", memory.get("health_score", 50))
    c2.metric("💧 Water", memory.get("water_intake", 0))
    c3.metric("⚡ Energy", memory.get("energy_level", 5))
    c4.metric("😴 Sleep", memory.get("sleep_hours", 0))

    memory.setdefault("daily_food_log", [])

    food_calories_today = sum(
        (entry.get("calories") or 0)
        for entry in memory["daily_food_log"]
    )

    c5.metric("🍛 Food Calories", food_calories_today)

    # ---------------- DAILY LOOP ELEMENTS ----------------
    gamification_ui(memory)
    morning_briefing_ui(memory)

    # ---------------- INTELLIGENCE BRAINS ----------------
    nutritionist_brain(memory)
    metabolic_predictor(memory)
    behavior_brain(memory)

    if memory.get("nutrition_insights"):
        st.subheader("🧠 AI Nutritionist Insights")
        for i in memory["nutrition_insights"]:
            st.info(i)

    if memory.get("metabolic_alerts"):
        st.subheader("🧬 Metabolic Health Signals")
        for a in memory["metabolic_alerts"]:
            st.warning(a)

    if memory.get("behavior_alerts"):
        st.subheader("🧠 Behavior Insights")
        for b in memory["behavior_alerts"]:
            st.warning(b)

    # ---------------- COST ----------------
    requests, usd, inr = get_cost_summary(memory)

    st.divider()
    st.subheader("💰 AI Usage Today")

    cc1, cc2, cc3 = st.columns(3)
    cc1.metric("Requests Used", requests)
    cc2.metric("USD Spent", f"${usd}")
    cc3.metric("Estimated Cost", f"₹{inr}")

    st.divider()

    # ---------------- CHECK-IN ----------------
    st.subheader("Daily Check-In")

    sleep = st.slider("Sleep Hours", 0, 12, memory.get("sleep_hours", 6))
    energy = st.slider("Energy", 1, 10, memory.get("energy_level", 5))
    exercise = st.checkbox("Exercise done", memory.get("exercise_done", False))
    water = st.number_input("Water glasses", 0, 20, memory.get("water_intake", 0))

    if st.button("Save Check-In"):

        memory["sleep_hours"] = sleep
        memory["energy_level"] = energy
        memory["exercise_done"] = exercise
        memory["water_intake"] = water

        memory.setdefault("daily_health_log", [])
        memory["daily_health_log"].append({
            "sleep": sleep,
            "energy": energy,
            "water": water,
            "exercise": exercise
        })

        calculate_health_score(memory)
        update_streak(memory)
        add_xp(memory)

        st.success("Check-in saved!")

        st.divider()

    # ❤️ EMOTIONAL REWARD ENGINE
emotional_reward_engine(memory)

if isinstance(memory.get("emotional_rewards"), list):
    st.subheader("❤️ Today's Wins")

    for reward in memory["emotional_rewards"]:
        st.success(reward)


    st.divider()

    # 🧠 IDENTITY ENGINE
    identity_engine_ui(memory)

    st.divider()

    health_master_brain(memory)


# =====================================================
# CHAT
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
# INSIGHTS
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
# PLANNER
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
# RECORDS
# =====================================================

with tab_records:
    health_record_vault()
    st.divider()
    prescription_reader_ui(memory)

# =====================================================
# ADMIN
# =====================================================

if st.session_state.user in ADMIN_USERS:
    with tab_admin:
        admin_dashboard()
        st.divider()
        admin_control_center(memory)

# =====================================================
# SAVE MEMORY
# =====================================================

save_memory(memory)
