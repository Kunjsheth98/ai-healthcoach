import streamlit as st
import math

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

# Intelligence Layers
from agents.nutritionist_brain import nutritionist_brain
from agents.metabolic_predictor import metabolic_predictor
from agents.behavior_brain import behavior_brain

# WhatsApp + notifications remain intact
from agents.smart_notifications import smart_notification_center

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
# GLOBAL STYLE + ANIMATION
# =====================================================
st.markdown("""
<style>
.block-container {max-width:900px;padding-top:1.5rem;}
*{transition:all .25s ease-in-out;}

.coach-card{
background:#111827;
padding:18px;
border-radius:14px;
color:white;
box-shadow:0 10px 25px rgba(0,0,0,.25);
}

.pulse{
width:8px;height:8px;background:#22c55e;
border-radius:50%;display:inline-block;
animation:pulse 1.5s infinite;margin-right:6px;
}

@keyframes pulse{
0%{opacity:1}
50%{opacity:.3}
100%{opacity:1}
}
</style>
""", unsafe_allow_html=True)

# =====================================================
# LOGIN
# =====================================================
if "user" not in st.session_state:
    st.session_state.user=None

if st.session_state.user is None:

    st.title("🔐 AI HealthCoach Login")
    tab1,tab2=st.tabs(["Login","Register"])

    with tab1:
        u=st.text_input("Username")
        p=st.text_input("Password",type="password")

        if st.button("Login"):
            if login_user(u,p):
                st.session_state.user=u
                st.rerun()
            else:
                st.error("Invalid credentials")

    with tab2:
        nu=st.text_input("New Username")
        np=st.text_input("New Password",type="password")

        if st.button("Register"):
            ok,msg=register_user(nu,np)
            st.success(msg) if ok else st.error(msg)

    st.stop()

# =====================================================
memory=load_memory()

st.title("🩺 AI HealthCoach")
st.caption(f"Logged in as: {st.session_state.user}")

# =====================================================
ADMIN_USERS=["demo"]

tabs=["🏠 Dashboard","💬 Coach","📊 Insights","🧭 Planner","🗂️ Records"]
if st.session_state.user in ADMIN_USERS:
    tabs.append("🛠️ Admin")

all_tabs=st.tabs(tabs)
tab_dashboard,tab_chat,tab_insights,tab_planner,tab_records=all_tabs[:5]
if st.session_state.user in ADMIN_USERS:
    tab_admin=all_tabs[5]

# =====================================================
# DASHBOARD
# =====================================================
with tab_dashboard:

    st.markdown("""
    <div class="coach-card">
    <h3>👩‍⚕️ Asha — Your AI Health Coach</h3>
    <p><span class="pulse"></span>Online • Learning from you daily</p>
    </div>
    """, unsafe_allow_html=True)

    # Metrics
    c1,c2,c3,c4=st.columns(4)
    c1.metric("Health Score",memory.get("health_score",50))
    c2.metric("Water",memory.get("water_intake",0))
    c3.metric("Energy",memory.get("energy_level",5))
    c4.metric("Sleep",memory.get("sleep_hours",0))

    # ================= PROGRESS RINGS =================
    st.subheader("📊 Daily Progress")

    def progress_ring(value,max_value,label):
        percent=min(value/max_value,1)
        angle=percent*360

        st.markdown(f"""
        <div style="
        width:120px;height:120px;border-radius:50%;
        background:conic-gradient(#22c55e {angle}deg,#1f2937 {angle}deg);
        display:flex;align-items:center;justify-content:center;margin:auto;">
            <div style="
            width:85px;height:85px;border-radius:50%;
            background:#0b0f19;color:white;
            display:flex;align-items:center;justify-content:center;
            font-weight:bold;">
            {int(percent*100)}%
            </div>
        </div>
        <p style="text-align:center">{label}</p>
        """,unsafe_allow_html=True)

    r1,r2,r3=st.columns(3)
    with r1: progress_ring(memory.get("sleep_hours",0),8,"Sleep")
    with r2: progress_ring(memory.get("water_intake",0),8,"Hydration")
    with r3: progress_ring(memory.get("energy_level",5),10,"Energy")

    st.divider()

    # Intelligence engines
    nutritionist_brain(memory)
    metabolic_predictor(memory)
    behavior_brain(memory)

    gamification_ui(memory)
    morning_briefing_ui(memory)
    smart_notification_center(memory)

    emotional_reward_engine(memory)
    identity_engine_ui(memory)
    health_master_brain(memory)

# =====================================================
# CHAT
# =====================================================
with tab_chat:

    chats=list_chats()
    chat_name=st.selectbox("Select Chat",chats if chats else ["default"])

    messages=load_chat(chat_name)

    for m in messages:
        st.chat_message(m["role"]).write(m["content"])

    user_msg=st.chat_input("Ask Asha...")

    if user_msg:
        messages.append({"role":"user","content":user_msg})
        reply=ask_health_coach(memory,user_msg,messages)
        messages.append({"role":"assistant","content":reply})
        save_chat(chat_name,messages)
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

    if has_premium_access("movement_coach"):
        movement_coach_agent(memory)
    else:
        premium_lock()

# =====================================================
# RECORDS
# =====================================================
with tab_records:
    health_record_vault()
    prescription_reader_ui(memory)

# =====================================================
# ADMIN
# =====================================================
if st.session_state.user in ADMIN_USERS:
    with tab_admin:
        admin_dashboard()
        admin_control_center(memory)

# =====================================================
save_memory(memory)
