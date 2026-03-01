import streamlit as st

# ================= AUTH =================
from core.auth import register_user, login_user
from datetime import timedelta, datetime
# ================= MEMORY =================
from core.memory import load_memory, save_memory

# ================= CHAT =================
from core.chat_manager import list_chats, load_chat, save_chat

# ================= SUBSCRIPTION =================
from core.subscription import has_premium_access, premium_lock

# ================= COST =================
from core.budget_guard import check_budget, register_ai_call, allow_request

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
from agents.daily_neural_sync import daily_neural_sync
from agents.stress_engine import stress_engine
from agents.system_state_engine import system_state_engine
from agents.hormonal_intelligence import hormonal_intelligence_core
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
st.markdown("""
<style>
.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
}
h2, h3 {
    margin-top: 0.8rem;
}
</style>
""", unsafe_allow_html=True)

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
                st.error("Invalid username or password")

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

# ================= LIFE OS STRATEGY =================

def generate_daily_strategy(memory):
    mode = memory.get("life_os_mode", "wellness")
    focus = memory.get("primary_intent", "general")
    burnout = memory.get("burnout_risk_level", 0)

    if burnout >= 70:
        return "Protect Recovery"

    if focus == "sleep":
        return "Stabilize Sleep"
    elif focus == "stress":
        return "Lower Nervous Load"
    elif focus == "movement":
        return "Build Physical Consistency"

    if mode == "performance":
        return "Push Performance"
    elif mode == "discipline":
        return "Execute Structure"
    elif mode == "resilience":
        return "Strengthen Stability"

    return "Maintain Balance"

st.title("🩺 Adaptive AI Health Coach")
st.caption("Sleep. Stress. Strength. Consistency.")
st.caption(f"Logged in as: {st.session_state.user}")

# ================= CHAT SIDEBAR =================

import uuid

st.sidebar.title("🧠 Your Health Plans")

# Load existing chats
chats = list_chats()

# Create new chat
if st.sidebar.button("➕ New Health Plan"):
    new_chat_id = str(uuid.uuid4())
    save_chat(new_chat_id, [])
    st.session_state.current_chat = new_chat_id

# Initialize current chat
if "current_chat" not in st.session_state:
    if chats:
        st.session_state.current_chat = chats[0]
    else:
        first_chat = str(uuid.uuid4())
        save_chat(first_chat, [])
        st.session_state.current_chat = first_chat

# Display chat list
for chat_id in chats:
    if st.sidebar.button(f"📂 {chat_id[:8]}", key=chat_id):
        st.session_state.current_chat = chat_id

# Load chat history
chat_history = load_chat(st.session_state.current_chat)

# =====================================================
# ADMIN USERS
# =====================================================
ADMIN_USERS = ["demo"]

tabs = [
    "🧠 Brain",
    "📥 Daily Sync",
    "🗣 Coach",
    "📅 Planner",
    "📊 Trends",
    "🗂 Vault",
]

if st.session_state.user in ADMIN_USERS:
    tabs.append("🛠️ Admin")

all_tabs = st.tabs(tabs)

tab_brain = all_tabs[0]
tab_sync = all_tabs[1]
tab_coach = all_tabs[2]
tab_planner = all_tabs[3]
tab_trends = all_tabs[4]
tab_vault = all_tabs[5]

if st.session_state.user in ADMIN_USERS:
    tab_admin = all_tabs[6]

# =====================================================
# DASHBOARD
# =====================================================
with tab_brain:

    # ================= CLEAN STRUCTURED ONBOARDING =================

    if not memory.get("onboarding_complete"):
        if "onboarding_step" not in memory:
            memory["onboarding_step"] = 1
        # ===============================
        # STEP 1 — BASIC INFO
        # ===============================

        if memory["onboarding_step"] == 1:

            st.markdown("### 👤 Basic Information")

            full_name = st.text_input("Full Name")
            age = st.number_input("Age", 10, 100, 25)
            gender = st.selectbox("Gender", ["Male", "Female", "Other"])
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

            if st.button("Next →"):

                memory["profile"] = {
                    "name": full_name,
                    "age": age,
                    "gender": gender,
                }

                memory.setdefault("lifestyle", {})
                memory["lifestyle"]["goal"] = goal_type

                memory["onboarding_step"] = 2
                save_memory(memory)
                st.rerun()


        # ===============================
        # STEP 2 — LIFESTYLE + CYCLE
        # ===============================

        elif memory["onboarding_step"] == 2:

            st.markdown("### 🧠 Lifestyle Profile")

            discipline = st.slider("How disciplined are you with routines?", 1, 10, 5)

            activity = st.selectbox(
                "Your activity type",
                ["Sedentary (desk work)", "Moderately active", "Very active"],
            )

            sleep_pattern = st.selectbox(
                "Your sleep pattern", ["Late sleeper", "Early riser", "Irregular"]
            )

            wake_time = st.time_input("Preferred wake-up time (optional)")

            gender = memory.get("profile", {}).get("gender")

            cycle_start = None
            cycle_length = 28

            if gender == "Female":
                cycle_start = st.date_input("Last Period Start Date")
                cycle_length = st.slider("Average Cycle Length (days)", 21, 35, 28)

            col1, col2 = st.columns(2)

            with col1:
                if st.button("← Back"):
                    memory["onboarding_step"] = 1
                    save_memory(memory)
                    st.rerun()

            with col2:
                if st.button("Complete Setup"):

                    memory["lifestyle"].update({
                        "discipline_score": discipline,
                        "activity_type": activity,
                        "sleep_pattern": sleep_pattern,
                        "preferred_wake_time": str(wake_time) if wake_time else None,
                    })

                    if gender == "Female" and cycle_start:
                        memory["cycle_tracking"] = {
                            "cycle_start_date": str(cycle_start),
                            "cycle_length": cycle_length
                        }

                    memory["onboarding_complete"] = True
                    memory["onboarding_step"] = 1
                    save_memory(memory)
                    st.rerun()

        st.stop()



    if memory.get("first_visit_done") != True:
        st.markdown("""
        ### 👋 Welcome to Your AI Health OS

        This system adapts daily based on:
        - Sleep
        - Energy
        - Stress
        - Movement

        Start with Daily Sync.
        Use Coach when stuck.
        Follow Planner for structure.
        """)
    
        if st.button("Start My Journey"):
            memory["first_visit_done"] = True
            save_memory(memory)
            st.rerun()

    strategy = generate_daily_strategy(memory)
    mode = memory.get("life_os_mode", "wellness")
    burnout = memory.get("burnout_risk_level", 0)
    system_state = memory.get("system_state", "balanced")

    color = "#16a34a"  # default green

    if system_state == "overloaded":
        color = "#dc2626"
    elif system_state == "recovery":
        color = "#f59e0b"
    elif mode == "performance":
        color = "#2563eb"
    elif mode == "discipline":
        color = "#7c3aed"
    elif mode == "resilience":
        color = "#0ea5e9"

    st.markdown(
        f"""
        <div style="
            padding:14px;
            border-radius:12px;
            background: linear-gradient(135deg,{color},#111827);
            box-shadow: 0px 4px 20px rgba(0,0,0,0.15);
            font-weight:600;
            margin-bottom:15px;">
            🎯 Today’s Strategy: {strategy}
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("---")


    st.markdown(f"""
        ### 🧠 Current System State
        * Strategic Focus: {memory.get("strategic_focus")}
        * Global Intensity: {memory.get("global_intensity_level")}
        * Identity Maturity: {memory.get("identity_maturity")}
        * Burnout Risk: {memory.get("burnout_risk_level")}
        """)

    from datetime import datetime

    st.header("🏠 Today")

    current_hour = datetime.now().hour

    if current_hour < 12:
        greeting = "Good morning"
    elif current_hour < 17:
        greeting = "Good afternoon"
    else:
        greeting = "Good evening"

    st.info(f"{greeting}. Let’s build consistency today.")

    if memory.get("streak_days", 0) >= 5:
        st.info("You’ve shown up consistently. Today matters.")

    # ---- Intent Selection (First Time Only) ----
    if "primary_intent" not in memory:

        st.subheader("What do you want to focus on today?")

        col1, col2, col3 = st.columns(3)

        if col1.button("😴 Fix Sleep"):
            memory["primary_intent"] = "sleep"

        if col2.button("🧘 Reduce Stress"):
            memory["primary_intent"] = "stress"

        if col3.button("🏋️ Start Movement"):
            memory["primary_intent"] = "movement"

    stress_engine(memory)
    system_state_engine(memory)
    hormonal_intelligence_core(memory)

    if memory.get("stress_recommendations"):
        st.subheader("🧠 Stress Recovery Suggestions")
    for r in memory.get("stress_recommendations", []):
        st.info(r)

    st.subheader("🧭 System Mode")

    state = memory.get("system_state", "balanced")

    if state == "overloaded":
        st.error("⚠ Overloaded Mode: Nervous system protection active.")

    elif state == "recovery":
        st.warning("🧘 Recovery Mode: Focus on nervous system reset.")

    elif state == "growth":
        st.success("🚀 Growth Mode: Capacity is high. Build forward.")

    else:
        st.info("⚖ Balanced Mode: Maintain steady progress.")    

    phase = memory.get("current_cycle_phase")

    if phase:

        phase_explanations = {
            "menstrual": "Low energy window. Focus on recovery and gentle movement.",
            "follicular": "Energy rising. Ideal time to build habits and intensity.",
            "ovulatory": "Peak performance window. Best for strength and confidence tasks.",
            "luteal": "Energy stabilizing. Reduce pressure and protect consistency."
        }

        explanation = phase_explanations.get(phase, "")

        cycle_day = memory.get("cycle_day")
        next_period = memory.get("next_period_estimate")

        st.markdown("---")
        st.subheader("🧬 Hormonal Intelligence")

        st.markdown(f"""
    *Current Phase:* {phase.capitalize()}  
    *Cycle Day:* {cycle_day}  
    *Next Period Estimate:* {next_period}

    {explanation}
    """)

    # ---- Companion Guided Intro ----
    if "companion_intro_shown" not in memory:

        st.markdown("### 👋 How This Works")

        st.write(
            """
            This is your AI Health Companion.

            1️⃣ Choose what you want to improve today.  
            2️⃣ I adapt your daily plan automatically.  
            3️⃣ Use Coach if you feel stuck.  
            4️⃣ Do Daily Sync once per day.
            """
        )

        if st.button("Got it"):
            memory["companion_intro_shown"] = True 
            save_memory (memory)

    # ===== LIFE OS COLOR STATE =====
    mode = memory.get("life_os_mode", "wellness")
    burnout = memory.get("burnout_risk_level", 0)

    color = "#16a34a"  # green default

    if burnout >= 70:
        color = "#dc2626"  # red
    elif burnout >= 40:
        color = "#f59e0b"  # orange
    elif mode == "performance":
        color = "#2563eb"
    elif mode == "discipline":
        color = "#7c3aed"
    elif mode == "resilience":
        color = "#0ea5e9"

    
    st.subheader("🧠 System Mode")
    st.info(f"Mode: {mode.upper()} | Burnout Risk: {burnout}")
    

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

    if memory.get("burnout_risk_level", 0) >= 7:
        st.error("🚨 Neural Burnout Engine Warning: Immediate recovery needed.")
    elif memory.get("burnout_risk_level", 0) >= 4:
        st.warning("⚠ Neural Burnout Rising. Adjust workload.")


    st.subheader("🧠 Life OS Mode")
    brain = memory.get("brain_state", {})
    mode = brain.get("mode", "wellness")
    st.info(memory.get("life_os_mode", "wellness").upper())
    st.success(memory.get("health_identity", "Not Classified Yet"))

    st.subheader("📱 WhatsApp Notifications")

    phone = st.text_input("Enter WhatsApp number", value=memory.get("phone_number", ""))

    if st.button("Save Number"):
        memory["phone_number"] = phone
        st.success("Number saved!")

    st.markdown("---")
    st.subheader("Today's Overview")
    if memory.get("daily_insight"):
        st.subheader("🧠 AI Insight")
        st.success(memory["daily_insight"])

    c1, c2, c3, c4, c5, c6, c7, c8 = st.columns(8)

    c1.metric("🧠 Health Score", memory.get("health_score", 50))
    from core.subscription import has_premium_access

    if has_premium_access("mental_engine"):
        c1.metric("🧠 Mental Score", memory.get("mental_score", 50))
    c2.metric("💧 Water", memory.get("water_intake", 0))
    c3.metric("⚡ Energy", memory.get("energy_level", 5))
    c4.metric("😴 Sleep", memory.get("sleep_hours", 0))

    identity = memory.get("identity_lock", {}).get("current_identity")

    if identity:
        st.subheader("🧠 Your Evolving Identity")
        st.success(identity)

    memory.setdefault("daily_food_log", [])
    food_calories_today = sum(
        (entry.get("calories") or 0) for entry in memory["daily_food_log"]
    )
    c5.metric("🍛 Food Calories", food_calories_today)
    c6.metric(
        "📉 Body Fat",
        f"{memory.get('body_fat_estimate', '—')}%"
    )
    c7.metric(
        "⚖️ Weight Trend (7d)",
        f"{memory.get('weight_trend_7d', 0)} kg"
    )
    c8.metric(
        "🧬 Hormonal Stress",
        memory.get("hormonal_stress_index", 0)
    )

    st.markdown("---")
    st.subheader("🔥 Consistency")

    st.metric("Current Streak", memory.get("streak_days", 0))

    if memory.get("streak_days", 0) >= 7:
        st.success("You’re building identity-level consistency.")
    elif memory.get("streak_days", 0) >= 3:
        st.info("Momentum forming. Protect it.")

    # ---------------- MENTAL HEALTH SECTION ----------------
    if has_premium_access("mental_engine"):

        st.markdown("---")
        st.subheader("🧠 Mental Health")

        m1, m2, m3 = st.columns(3)

        m1.metric("Stress Index", memory.get("stress_index", 5))
        m2.metric("Anxiety Index", memory.get("anxiety_index", 5))
        m3.metric("Burnout Risk", memory.get("burnout_risk_level", 0))

        burnout = memory.get("burnout_risk_level", 0)
        if burnout >= 7:
            st.error("🚨 High Burnout Risk Detected. Immediate recovery protocol recommended.")
        elif burnout >= 4:
            st.warning("⚠ Moderate Burnout Signals. Reduce workload and increase recovery.")

    if memory.get("risk_forecast"):
        prob = memory["risk_forecast"].get("burnout_probability", 0)
        st.info(f"🧠 Burnout Prediction Risk: {int(prob*100)}%")   

        st.subheader("🧠 AI Brain Status")
        st.info(f"Mode: {mode}")

        forecast = memory.get("risk_forecast", {})
        st.metric("Burnout Forecast", f"{int(forecast.get('burnout_probability',0)*100)}%")
        st.caption(f"Trigger: {forecast.get('primary_trigger','Stable')}") 

    # ===============================
    # 📈 Body Fat Trend Chart
    # ===============================

    bf_history = memory.get("body_fat_history", [])

    if len(bf_history) >= 2:
        st.subheader("📈 Body Fat Trend")

        import pandas as pd
        from datetime import datetime, timedelta

        dates = [
            datetime.now().date() - timedelta(days=len(bf_history)-i-1)
            for i in range(len(bf_history))
        ]

        df = pd.DataFrame({
            "Date": dates,
            "Body Fat %": bf_history
        })

        st.line_chart(df.set_index("Date"))

    import pandas as pd
    from datetime import datetime, timedelta

    dates = [
        datetime.now().date() - timedelta(days=len(bf_history)-i-1)
        for i in range(len(bf_history))
    ]

    df = pd.DataFrame({
        "Date": dates,
        "Body Fat %": bf_history
    })

    st.line_chart(df.set_index("Date"))  

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
        sleep_hours = memory.get("sleep_hours", 0)
        # Cap sleep at 7 for scoring psychology
        sleep_hours = memory.get("sleep_hours", 0)
        sleep_percentage = min(int((sleep_hours / 8) * 100), 100)

        progress_ring(sleep_percentage, 100, "Sleep")

    with r2:
        progress_ring(memory.get("water_intake", 0), 8, "Hydration")

    with r3:
        progress_ring(memory.get("energy_level", 5), 10, "Energy")

    # ---------------- FIRST DAY HOOK ENGINE ----------------

    classify_health_identity(memory)
    generate_pattern_reflection(memory)
    generate_future_projection(memory)

    st.subheader("🔮 Your Health Intelligence")

    if memory.get("pattern_insights"):
        st.info(memory["pattern_insights"][-1])

    if memory.get("future_projection"):
        st.warning(memory["future_projection"])

    if memory.get("emotional_rewards"):
        st.success(memory["emotional_rewards"][-1])

    st.subheader("🧬 Your Health Identity")
    st.success(memory.get("health_identity", ""))

    if memory.get("pattern_insights"):
        st.subheader("🧠 What Your Health Pattern Shows")
        for insight in memory.get("pattern_insights", []):
            st.info(insight)

    if memory.get("future_projection"):
        st.subheader("🔮 Health Outlook")
        st.warning(memory["future_projection"])


    if memory.get("nutrition_insights"):
        st.subheader("🧠 AI Nutritionist Insights")
        for i in memory.get("nutrition_insights", []):
            st.info(i)

    if memory.get("metabolic_alerts"):
        st.subheader("🧬 Metabolic Health Signals")
        for a in memory.get("metabolic_alerts", []):
            st.warning(a)

    if memory.get("behavior_alerts"):
        st.subheader("🧠 Behavior Insights")
        for b in memory.get("behavior_alerts", []):
            st.warning(b)

    st.markdown("---")
    st.subheader("💰 AI Usage Today")

    cost = memory.get("budget", {}).get("daily_cost", 0)
    st.metric("USD Spent Today", round(cost, 3))

    st.markdown("---")

    emotional_reward_engine(memory)

    if memory.get("emotional_rewards"):
        st.success(memory["emotional_rewards"][-1])

    st.markdown("---")

    identity_engine_ui(memory)
    st.markdown("---")

    st.subheader("📊 Today Summary")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Sleep", f"{memory.get('sleep_hours', 0)} hrs")

    with col2:
        st.metric("Energy", memory.get("energy_level", 0))

    with col3:
        st.metric("Mood", memory.get("daily_mood", 0))

    st.markdown("---")

    st.subheader("🧠 Current State")

    sleep = memory.get("sleep_hours", 0)
    energy = memory.get("energy_level", 0)
    mood = memory.get("daily_mood", 0)

    state_messages = []

    # Sleep interpretation
    if sleep <= 4:
        state_messages.append("⚠️ Sleep debt detected. Prioritize recovery.")
    elif sleep <= 6:
        state_messages.append("😐 Moderate sleep. Avoid pushing too hard.")
    else:
        state_messages.append("✅ Well rested. Body ready.")

    # Energy interpretation
    if energy <= 4:
        state_messages.append("🔋 Low energy window.")
    elif energy <= 7:
        state_messages.append("⚖️ Balanced energy.")
    else:
        state_messages.append("🔥 High output window.")

    # Mood interpretation
    if mood <= 4:
        state_messages.append("💛 Emotional care recommended.")
    elif mood <= 7:
        state_messages.append("🙂 Stable emotional state.")
    else:
        state_messages.append("🌟 Positive emotional momentum.")

    if memory.get("stress_score", 0) >= 4:
        st.error("⚠ High stress detected. Prioritize recovery.")
    elif memory.get("stress_score", 0) >= 2:
        st.warning("Moderate stress. Stay mindful today.")
    else:
        st.success("Stable state. Keep building.")

    streak = memory.get("streak_days", 0)

    if streak >= 7:
        st.info("Your nervous system adapts faster when consistency is high.")
    elif streak >= 3:
        st.info("Consistency builds biological stability.")    

    for msg in state_messages:
        st.write(msg)

    st.markdown("---")

    focus = memory.get("primary_intent", "general")

    if focus == "sleep":
        st.info("Your focus is sleep stabilization. Protect your night.")
    elif focus == "stress":
        st.info("Today is about lowering pressure, not increasing output.")
    elif focus == "movement":
        st.info("Small movement done daily beats intensity.")
    else:
        st.info("Build consistency first. Intensity comes later.")

    st.markdown("---")

    health_master_brain(memory)

    if memory.get("system_intervention"):
        st.info(memory["system_intervention"])


with tab_sync:

    strategy = generate_daily_strategy(memory)
    mode = memory.get("life_os_mode", "wellness")
    burnout = memory.get("burnout_risk_level", 0)
    system_state = memory.get("system_state", "balanced")

    color = "#16a34a"  # default green

    if system_state == "overloaded":
        color = "#dc2626"
    elif system_state == "recovery":
        color = "#f59e0b"
    elif mode == "performance":
        color = "#2563eb"
    elif mode == "discipline":
        color = "#7c3aed"
    elif mode == "resilience":
        color = "#0ea5e9"

    st.markdown(
        f"""
        <div style="
            padding:14px;
            border-radius:12px;
            background: linear-gradient(135deg,{color},#111827);
            box-shadow: 0px 4px 20px rgba(0,0,0,0.15);
            font-weight:600;
            margin-bottom:15px;">
            🎯 Today’s Strategy: {strategy}
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("---")


    st.header("🔄 Daily Sync")

    from datetime import datetime
    today = datetime.now().date()
    last_checkin = memory.get("last_checkin_date")

    if last_checkin == str(today):
        st.warning("✅ You've already completed today's check-in.")
        st.stop()
    sleep_hours = st.number_input(
        "🛌 How many hours did you sleep last night?",
        min_value=0.0,
        max_value=12.0,
        step=0.5
    )
    energy = st.slider(
        "⚡ How energetic do you feel right now?",
        min_value=1,
        max_value=10,
        help="1 = exhausted, 10 = fully energized"
    )

    mood = st.slider("Mood Today (1 = Very Low, 10 = Excellent)", 
                 1, 10, 
                 memory.get("daily_mood", 5))
    
    st.caption("Exercise: Did you complete any planned movement today?")
    exercise = st.checkbox("Exercise done", memory.get("exercise_done", False))
    water = st.slider(
        "💧 How many glasses of water have you had today?",
        min_value=0,
        max_value=15,
        help="1 glass ≈ 250ml"
    )
    emotion = st.selectbox(
        "🧠 How are you feeling emotionally?",
        ["stable", "anxious", "low", "overwhelmed", "motivated"]
    )

    if st.button("Save Check-In"):
        memory["daily_mood"] = mood
        memory.setdefault("emotional_event_log", [])
        memory["emotional_event_log"].append({
            "mood": mood,
            "sleep": sleep_hours,
            "energy": energy
        })
        memory["sleep_hours"] = sleep_hours
        memory["energy_level"] = energy
        memory["exercise_done"] = exercise
        memory["water_intake"] = water
        memory["last_checkin_date"] = str(today)
        memory["emotion_state"] = emotion
        st.markdown("---")

    nutritionist_brain(memory)
    metabolic_predictor(memory)
    behavior_brain(memory)
    medicine_reminder_agent(memory)

    st.markdown("---")

    st.subheader("📸 Upload Food Image")
    food_image = st.file_uploader("Upload meal photo")

    if food_image:
        from agents.food_vision_engine import analyze_food_image

        result = analyze_food_image(food_image, memory)
        st.info(result)


        # ---- Track Weight History ----
        current_weight = memory.get("profile", {}).get("weight_kg")

        if current_weight:
            memory.setdefault("weight_history", [])
            memory["weight_history"].append({"weight": current_weight})
            memory["weight_history"] = memory["weight_history"][-30:]
            memory.setdefault("daily_health_log", [])
            memory["daily_health_log"].append(
            {"sleep": sleep, "energy": energy, "water": water, "exercise": exercise}
            )

        memory["engagement_score"] = memory.get("engagement_score", 0) + 1

        add_xp(memory)
        update_streak(memory)
        if memory["engagement_score"] % 5 == 0:
            st.success("🔥 Amazing consistency! Your future self is proud of you.")
        calculate_health_score(memory)
        daily_neural_sync(memory)
        from agents.habit_reinforcement_engine import neural_habit_engine
        neural_habit_engine(memory)
        st.success("Check-in saved!")

        if memory.get("streak_days", 0) >= 1:
            st.success("🔥 Another brick added to your future self.")

        if memory.get("streak_days", 0) % 5 == 0 and memory.get("streak_days", 0) > 0:
            st.success("🏆 Milestone reached. Identity strengthening.")  


# =====================================================
# CHAT / INSIGHTS / PLANNER / RECORDS / ADMIN
# =====================================================
# (UNCHANGED — EXACT SAME AS YOUR VERSION)

with tab_coach:

    strategy = generate_daily_strategy(memory)
    mode = memory.get("life_os_mode", "wellness")
    burnout = memory.get("burnout_risk_level", 0)
    system_state = memory.get("system_state", "balanced")

    color = "#16a34a"  # default green

    if system_state == "overloaded":
        color = "#dc2626"
    elif system_state == "recovery":
        color = "#f59e0b"
    elif mode == "performance":
        color = "#2563eb"
    elif mode == "discipline":
        color = "#7c3aed"
    elif mode == "resilience":
        color = "#0ea5e9"

    st.markdown(
        f"""
        <div style="
            padding:14px;
            border-radius:12px;
            background: linear-gradient(135deg,{color},#111827);
            box-shadow: 0px 4px 20px rgba(0,0,0,0.15);
            font-weight:600;
            margin-bottom:15px;">
            🎯 Today’s Strategy: {strategy}
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("---")


    st.header("💬 Coach")

    st.markdown("---")
    st.subheader("🪞 Future Self Insight")

    streak = memory.get("streak_days", 0)

    if streak >= 7:
        st.success("Your future self is proud of this version of you.")
    elif streak >= 3:
        st.info("You’re building consistency. Protect it.")
    else:
        st.warning("Your future self needs action today.")

    st.subheader("🧑‍⚕️ Your AI Coach")

    st.caption("Use Coach to ask about sleep, stress, diet, workouts, or emotional clarity.")
    st.caption("Coach adapts based on your Daily Sync and lifestyle profile.")
    # ---- Guided Entry Prompts ----
    if "coach_prompt_shown" not in memory:

        intent = memory.get("primary_intent", "general")

        if intent == "sleep":
            suggestion = "Want a 7-day sleep reset plan?"
        elif intent == "stress":
            suggestion = "Feeling overwhelmed? Want a 3-minute reset?"
        elif intent == "movement":
            suggestion = "Want a beginner movement routine?"
        else:
            suggestion = "Tell me what you're struggling with today."

        st.info(suggestion)

        if st.button("Yes, help me"):
            memory["coach_auto_message"] = suggestion
            memory["coach_prompt_shown"] = True
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
        with st.chat_message(m.get("role", "assistant")):
            st.write(m.get("content", ""))
            if m.get("role") == "assistant":
                st.caption(f"AI Confidence: {memory.get('last_ai_confidence', 80)} %")
            if memory.get("behavior_drift"):
                 st.caption("⚠️ Behavior drift detected")  
            if memory.get("future_projection_state"):
                st.caption(f"🔮 Forecast: {memory.get('future_projection_state')}")     
            if memory.get("evolution_stage"):
                st.caption(f"🧬 Evolution Stage: {memory.get('evolution_stage')}")
            if memory.get("active_prompt_style"):
                st.caption(f"🧠 Adaptive Style: {memory.get('active_prompt_style')}") 
            if memory.get("meta_strategy"):
                st.caption(f"🧠 Meta Strategy: {memory.get('meta_strategy')}")      
            if memory.get("reflex_alert"):
                st.caption("⚡ Reflex Mode Activated")    
            if memory.get("variable_reward") == "bonus_encouragement":
                st.caption("🎉 Bonus Momentum Reward Unlocked")         

    # Chat input ALWAYS renders
    uploaded_image = st.file_uploader("Upload image (optional)", key="chat_img")
    user_msg = st.chat_input("Ask Asha...")
    # ---- Auto-trigger Coach Message ----
    if memory.get("coach_auto_message"):
        auto_msg = memory.pop("coach_auto_message")
        user_msg = auto_msg

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


with tab_trends:

    strategy = generate_daily_strategy(memory)
    mode = memory.get("life_os_mode", "wellness")
    burnout = memory.get("burnout_risk_level", 0)
    system_state = memory.get("system_state", "balanced")

    color = "#16a34a"  # default green

    if system_state == "overloaded":
        color = "#dc2626"
    elif system_state == "recovery":
        color = "#f59e0b"
    elif mode == "performance":
        color = "#2563eb"
    elif mode == "discipline":
        color = "#7c3aed"
    elif mode == "resilience":
        color = "#0ea5e9"

    st.markdown(
        f"""
        <div style="
            padding:14px;
            border-radius:12px;
            background: linear-gradient(135deg,{color},#111827);
            box-shadow: 0px 4px 20px rgba(0,0,0,0.15);
            font-weight:600;
            margin-bottom:15px;">
            🎯 Today’s Strategy: {strategy}
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("---")


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

    st.subheader("🔮 7-Day Projection")

    sleep = memory.get("sleep_hours", 0)
    energy = memory.get("energy_level", 0)
    mood = memory.get("daily_mood", 0)

    projection = ""

    # Projection logic
    if sleep <= 4 and energy <= 4:
        projection = "If this continues for 7 days, burnout probability increases significantly."
    elif sleep <= 6:
        projection = "In 7 days, mild fatigue accumulation may appear."
    elif energy >= 8 and sleep >= 7:
        projection = "In 7 days, performance momentum will compound."
    elif mood <= 4:
        projection = "Emotional exhaustion risk increases within a week."
    else:
        projection = "Current pattern is stable. Small improvements will compound."

    st.warning(projection)

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

    strategy = generate_daily_strategy(memory)
    mode = memory.get("life_os_mode", "wellness")
    burnout = memory.get("burnout_risk_level", 0)
    system_state = memory.get("system_state", "balanced")

    color = "#16a34a"  # default green

    if system_state == "overloaded":
        color = "#dc2626"
    elif system_state == "recovery":
        color = "#f59e0b"
    elif mode == "performance":
        color = "#2563eb"
    elif mode == "discipline":
        color = "#7c3aed"
    elif mode == "resilience":
        color = "#0ea5e9"

    st.markdown(
        f"""
        <div style="
            padding:14px;
            border-radius:12px;
            background: linear-gradient(135deg,{color},#111827);
            box-shadow: 0px 4px 20px rgba(0,0,0,0.15);
            font-weight:600;
            margin-bottom:15px;">
            🎯 Today’s Strategy: {strategy}
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("---")


    st.subheader("🏆 Growth Status")

    streak = memory.get("streak_days", 0)

    if streak < 3:
        rank = "Beginner"
    elif streak < 7:
        rank = "Committed"
    elif streak < 21:
        rank = "Disciplined"
    elif streak < 45:
        rank = "Elite"
    else:
        rank = "Unbreakable"

    st.success(f"Current Rank: {rank}")

    gamification_ui(memory)
    autonomous_planner_agent(memory)
    if memory.get("structured_plan"):
        tomorrow = (datetime.now() + timedelta(days=1)).strftime("%A")
        st.subheader(f"📅 Tomorrow Plan — {tomorrow}")
        st.markdown(memory["structured_plan"])
        st.caption("This plan adapts to your sleep, stress, burnout risk, and identity stage.")

    if has_premium_access("adaptive_planner"):
        adaptive_life_planner(memory)
    else:
        premium_lock()

    st.markdown("---")

    if has_premium_access("movement_coach"):
        movement_coach_agent(memory)
    else:
        premium_lock()

with tab_vault:
    strategy = generate_daily_strategy(memory)
    mode = memory.get("life_os_mode", "wellness")
    burnout = memory.get("burnout_risk_level", 0)
    system_state = memory.get("system_state", "balanced")

    color = "#16a34a"  # default green

    if system_state == "overloaded":
        color = "#dc2626"
    elif system_state == "recovery":
        color = "#f59e0b"
    elif mode == "performance":
        color = "#2563eb"
    elif mode == "discipline":
        color = "#7c3aed"
    elif mode == "resilience":
        color = "#0ea5e9"

    st.markdown(
        f"""
        <div style="
            padding:14px;
            border-radius:12px;
            background: linear-gradient(135deg,{color},#111827);
            box-shadow: 0px 4px 20px rgba(0,0,0,0.15);
            font-weight:600;
            margin-bottom:15px;">
            🎯 Today’s Strategy: {strategy}
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("---")

    health_record_vault()
    st.markdown("---")
    prescription_reader_ui(memory)

if st.session_state.user in ADMIN_USERS:
    tab_admin = all_tabs[-1]   # last tab is admin
    with tab_admin:
        admin_dashboard()
        st.markdown("---")
        admin_control_center(memory)

save_memory(memory)
