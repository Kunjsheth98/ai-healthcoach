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

from agents.nutritionist_brain import nutritionist_brain
from agents.metabolic_predictor import metabolic_predictor
from agents.behavior_brain import behavior_brain

from agents.health_identity import classify_health_identity
from agents.pattern_reflection import generate_pattern_reflection
from agents.future_projection import generate_future_projection
from agents.medicine_reminder import medicine_reminder_agent

from agents.voice_engine import speak_text
from agents.body_composition import calculate_body_fat

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
st.set_page_config(page_title="AI HealthCoach", page_icon="🩺", layout="wide")

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

tabs = [
    "🏠 Dashboard",
    "💬 Coach",
    "🧠 Mental",
    "📊 Insights",
    "🧭 Planner",
    "🗂️ Records",
]

if st.session_state.user in ADMIN_USERS:
    tabs.append("🛠️ Admin")

all_tabs = st.tabs(tabs)

tab_dashboard, tab_chat, tab_mental, tab_insights, tab_planner, tab_records = all_tabs[
    :6
]

if st.session_state.user in ADMIN_USERS:
    tab_admin = all_tabs[5]

# =====================================================
# DASHBOARD
# =====================================================
with tab_dashboard:

    # ================= CLEAN STRUCTURED ONBOARDING =================

    if not memory.get("onboarding_complete"):

        st.subheader("🧬 Let's Build Your Health Profile")

        st.markdown("### 👤 Basic Information")

        full_name = st.text_input("Full Name")
        age = st.number_input("Age", 10, 100, 25)
        gender = st.selectbox("Gender", ["Male", "Female", "Other"])
        height = st.number_input("Height (cm)", 100, 220, 170)
        weight = st.number_input("Weight (kg)", 30, 200, 70)

        diseases = st.multiselect(
            "Any Known Medical Conditions?",
            ["Diabetes", "Thyroid", "Hypertension", "PCOS", "Heart Issues", "Asthma"],
        )

        medications = st.text_input("Current Medications (optional)")

        st.markdown("### 🧠 Lifestyle Profile")

        discipline = st.slider("How disciplined are you with routines?", 1, 10, 5)
        stress = st.slider("Current stress level?", 1, 10, 5)

        activity = st.selectbox(
            "Your activity type",
            ["Sedentary (desk work)", "Moderately active", "Very active"],
        )

        sleep_pattern = st.selectbox(
            "Your sleep pattern", ["Late sleeper", "Early riser", "Irregular"]
        )

        goal_type = st.selectbox(
            "Main health goal",
            [
                "Fat loss",
                "Muscle gain",
                "Energy boost",
                "Stress reduction",
                "General fitness",
            ],
        )

        if st.button("Complete Setup"):

            memory["profile"] = {
                "name": full_name,
                "age": age,
                "gender": gender,
                "height_cm": height,
                "weight_kg": weight,
                "diseases": diseases,
                "medications": medications,
            }

            memory["lifestyle"] = {
                "discipline_score": discipline,
                "stress_level": stress,
                "activity_type": activity,
                "sleep_pattern": sleep_pattern,
                "goal": goal_type,
            }

            memory["onboarding_complete"] = True

            st.success("Profile Created Successfully ✅")
            save_memory(memory)
            st.rerun()

        st.stop()

    calculate_body_fat(memory)
    if memory.get("body_fat_percentage"):
        st.metric("🧬 Body Fat %", memory["body_fat_percentage"])

        from datetime import date

        today = str(date.today())
        profile = memory.get("profile", {})
        name = profile.get("name", st.session_state.user)

        if memory.get("last_greeted_date") != today:
            st.success(f"👋 Good to see you today, {name}!")
            memory["last_greeted_date"] = today
            save_memory(memory)

    # ---------- GRADIENT HERO ----------
    st.markdown(
        """
    <style>
    .hero {
        padding:20px;
        border-radius:15px;
        background: linear-gradient(135deg,#0f2027,#203a43,#2c5364);
        color:white;
        margin-bottom:20px;
    }
    </style>
    """,
        unsafe_allow_html=True,
    )

    st.markdown(
        f"""
        <div class="hero">
        <h2>👋 Welcome back {st.session_state.user}</h2>
        <h3>Health Score: {memory.get("health_score",50)}</h3>
        </div>
    """,
        unsafe_allow_html=True,
    )

    st.markdown(
        f"""
        <div style="
        padding:20px;
        border-radius:15px;
        background: linear-gradient(135deg,#0f2027,#203a43,#2c5364);
        color:white;
        margin-bottom:15px;">
        <h2>👩‍⚕️ Asha — Your AI Health Coach</h2>
        <p>Online • Learning from you daily</p>
        <h3>Health Score: {memory.get("health_score",50)}</h3>
        </div>
    """,
        unsafe_allow_html=True,
    )

    st.subheader("🏷 Your Health Identity")
    st.success(memory.get("health_identity", "Not Classified Yet"))

    st.subheader("📱 WhatsApp Notifications")

    phone = st.text_input("Enter WhatsApp number", value=memory.get("phone_number", ""))

    if st.button("Save Number"):
        memory["phone_number"] = phone
        st.success("Number saved!")

    st.divider()

    st.subheader("Today's Overview")

    c1, c2, c3, c4, c5 = st.columns(5)

    c1.metric("🧠 Health Score", memory.get("health_score", 50))
    from core.subscription import has_premium_access

    if has_premium_access("mental_engine"):
        st.metric("🧠 Mental Score", memory.get("mental_score", 50))
    c2.metric("💧 Water", memory.get("water_intake", 0))
    c3.metric("⚡ Energy", memory.get("energy_level", 5))
    c4.metric("😴 Sleep", memory.get("sleep_hours", 0))

    memory.setdefault("daily_food_log", [])
    food_calories_today = sum(
        (entry.get("calories") or 0) for entry in memory["daily_food_log"]
    )
    c5.metric("🍛 Food Calories", food_calories_today)
    # ---------------- MENTAL HEALTH SECTION ----------------
    if has_premium_access("mental_engine"):

        st.divider()
        st.subheader("🧠 Mental Health")

        m1, m2, m3 = st.columns(3)

        m1.metric("Stress Index", memory.get("stress_index", 5))
        m2.metric("Anxiety Index", memory.get("anxiety_index", 5))
        m3.metric("Burnout Risk", memory.get("burnout_risk_level", 0))

    if memory.get("burnout_risk_level", 0) >= 7:
        st.error("⚠️ High Burnout Risk Detected. Consider rest and stress reset.")
    elif memory.get("burnout_risk_level", 0) >= 4:
        st.warning("⚡ Moderate Burnout Signals Detected.")

    if memory.get("risk_forecast"):
        prob = memory["risk_forecast"].get("burnout_probability", 0)
        st.info(f"🧠 Burnout Prediction Risk: {int(prob*100)}%")    

        def progress_ring(value, max_value, label):
            percent = min(value / max_value, 1)
            angle = percent * 360

            st.markdown(
                f"""
            <div style="
                width:120px;height:120px;border-radius:50%;
                background:conic-gradient(#22c55e {angle}deg,#1f2937 {angle}deg);
                display:flex;align-items:center;justify-content:center;margin:auto;">
            <div style="
                width:85px;height:85px;background:#0b0f19;
                border-radius:50%;display:flex;
                align-items:center;justify-content:center;color:white;">
                {int(percent*100)}%
            </div>
            </div>
            <p style="text-align:center">{label}</p>
        """,
                unsafe_allow_html=True,
            )

    r1, r2, r3 = st.columns(3)

    with r1:
        progress_ring(memory.get("sleep_hours", 0), 8, "Sleep")

    with r2:
        progress_ring(memory.get("water_intake", 0), 8, "Hydration")

    with r3:
        progress_ring(memory.get("energy_level", 5), 10, "Energy")

    # ---------------- FIRST DAY HOOK ENGINE ----------------

    classify_health_identity(memory)
    generate_pattern_reflection(memory)
    generate_future_projection(memory)

    st.subheader("🧬 Your Health Identity")
    st.success(memory.get("health_identity", ""))

    if memory.get("first_day_insights"):
        st.subheader("🧠 What Your Health Pattern Shows")
        for insight in memory["first_day_insights"]:
            st.info(insight)

    if memory.get("future_projection"):
        st.subheader("🔮 Health Outlook")
        st.warning(memory["future_projection"])

    gamification_ui(memory)
    morning_briefing_ui(memory)
    nutritionist_brain(memory)
    metabolic_predictor(memory)
    behavior_brain(memory)
    medicine_reminder_agent(memory)

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

    requests, usd, inr = get_cost_summary(memory)

    st.divider()
    st.subheader("💰 AI Usage Today")

    cc1, cc2, cc3 = st.columns(3)
    cc1.metric("Requests Used", requests)
    cc2.metric("USD Spent", f"${usd}")
    cc3.metric("Estimated Cost", f"₹{inr}")

    st.divider()
    st.subheader("📸 Upload Food Image")

    food_image = st.file_uploader("Upload meal photo")

    if food_image:
        from agents.food_vision_engine import analyze_food_image

        result = analyze_food_image(food_image, memory)
        st.info(result)

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

        # ---- Track Weight History ----
    current_weight = memory.get("profile", {}).get("weight_kg")

    if current_weight:
        memory.setdefault("weight_history", [])
        memory["weight_history"].append({"weight": current_weight})

        memory.setdefault("daily_health_log", [])
        memory["daily_health_log"].append(
            {"sleep": sleep, "energy": energy, "water": water, "exercise": exercise}
        )

        calculate_health_score(memory)
        update_streak(memory)
        add_xp(memory)

        st.success("Check-in saved!")

    emotional_reward_engine(memory)

    if memory.get("emotional_rewards"):
        st.subheader("❤️ Today's Wins")
        for reward in memory["emotional_rewards"]:
            st.success(reward)

    st.divider()

    identity_engine_ui(memory)
    st.divider()

    health_master_brain(memory)

# =====================================================
# CHAT / INSIGHTS / PLANNER / RECORDS / ADMIN
# =====================================================
# (UNCHANGED — EXACT SAME AS YOUR VERSION)

with tab_chat:

    reply = ""

    chats = list_chats()

    chat_name = st.selectbox("Select Chat", chats if chats else ["default"])

    # Safe chat loading
    try:
        messages = load_chat(chat_name) or []
    except Exception:
        messages = []

    # Show chat history
    for m in messages:
        st.chat_message(m.get("role", "assistant")).write(m.get("content", ""))

    # Chat input ALWAYS renders
    uploaded_image = st.file_uploader("Upload image (optional)", key="chat_img")
    user_msg = st.chat_input("Ask Asha...")

    if user_msg:

        try:
            reply = ask_health_coach(memory, user_msg, messages.copy(), uploaded_image)
        except Exception:
            # Offline fallback (no API billing)
            reply = (
                "⚠️ Asha is currently in offline mode.\n\n"
                "AI responses are paused because API billing "
                "is not active."
            )

        messages.append({"role": "user", "content": user_msg})
        messages.append({"role": "assistant", "content": reply})
        st.session_state.last_reply = reply

        save_chat(chat_name, messages)
        st.rerun()

    language = st.selectbox("Voice Language", ["en", "hi", "mr", "ta"], index=0)

    if st.button("🔊 Hear Reply"):
        if "last_reply" in st.session_state:
            speak_text(st.session_state.last_reply, language)

with tab_mental:

    if has_premium_access("mental_engine"):

        st.subheader("🧠 Advanced Mental Health Intelligence")

        col1, col2 = st.columns(2)

        col1.metric("Mental Score", memory.get("mental_score", 50))
        col1.metric("Resilience Score", memory.get("resilience_score", 50))

        col2.metric("Stress Index", memory.get("stress_index", 5))
        col2.metric("Anxiety Index", memory.get("anxiety_index", 5))

        st.metric("Motivation Level", memory.get("motivation_level", 5))
        st.metric("Burnout Risk", memory.get("burnout_risk_level", 0))

        if memory.get("mental_history"):
            st.subheader("Recent Mental Trends")
            st.write(memory["mental_history"][-5:])

    else:
        premium_lock()


with tab_insights:

    # ---------------- MENTAL SCORE GRAPH ----------------
    if has_premium_access("mental_engine"):

        import matplotlib.pyplot as plt

        mental_history = memory.get("mental_history", [])

        if mental_history:
            scores = [entry.get("mental_score", 50) for entry in mental_history]

            fig, ax = plt.subplots()
            ax.plot(scores)
            ax.set_title("Mental Score Trend")
            ax.set_ylabel("Score")
            ax.set_xlabel("Check-ins")

            st.pyplot(fig)

        sleep_log = memory.get("daily_health_log", [])
        mental_log = memory.get("mental_history", [])

        if sleep_log and mental_log:

            sleep_values = [d.get("sleep", 0) for d in sleep_log]
            mental_scores = [m.get("mental_score", 50) for m in mental_log]

        if len(sleep_values) == len(mental_scores):

            fig, ax = plt.subplots()
            ax.plot(sleep_values, label="Sleep")
            ax.plot(mental_scores, label="Mental Score")
            ax.legend()

            st.pyplot(fig)        

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

with tab_records:
    health_record_vault()
    st.divider()
    prescription_reader_ui(memory)

if st.session_state.user in ADMIN_USERS:
    tab_admin = all_tabs[-1]   # last tab is admin
    with tab_admin:
        admin_dashboard()
        st.divider()
        admin_control_center(memory)

save_memory(memory)
