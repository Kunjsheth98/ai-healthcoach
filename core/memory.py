import json
import os
import streamlit as st
from core.database import get_connection
# =====================================================
# DEFAULT MEMORY STRUCTURE (USER AI BRAIN)
# =====================================================

DEFAULT_MEMORY = {
    "name": "",
    "health_goals": "",
    "phone_number": "",
    "onboarding_complete": False,
    # Health metrics
    "health_score": 50,
    "water_intake": 0,
    "sleep_hours": 7,
    "energy_level": 5,
    "exercise_done": False,
    # Tracking
    "calories_today": 0,
    "checkin_history": [],
    "weekly_report_date": "",
    "weekly_story": "",
    # Habit Brain
    "habit_log": [],
    "personality_mode": "balanced",
    # Emotional Engine
    "emotional_state": "balanced",
    # Personality Identity
    "personality_type": "adaptive",
    "personality_score": 50,
    # ================= ADVANCED MENTAL SYSTEM =================
    "mental_score": 50,
    "stress_index": 5,
    "anxiety_index": 5,
    "motivation_level": 5,
    "emotional_volatility": 0,
    "burnout_risk_level": 0,
    "behavior_profile": {},
    "trigger_patterns": [],
    "coping_style": "",
    "dominant_thought_patterns": [],
    "resilience_score": 50,
    "mental_history": [],
    "burnout_alerts": [],
    # ================= GAMIFICATION =================
    "streak_days": 0,
    "last_checkin_date": "",
    "xp_points": 0,
    "health_level": 1,
    # SMART REMINDERS
    "last_reminder_check": "",
    "reminder_log": [],
    # MORNING BRIEFING
    "last_briefing_date": "",
    "morning_briefing": "",
    # MEDICINE TRACKING
    "medicines": [],
    # MEDICINE REMINDERS
    "medicine_schedule": [],
    "last_medicine_check": "",
    # HEALTH RISK ANALYSIS
    "risk_history": [],
    "last_risk_check": "",
    # PERSONAL HEALTH TWIN
    "health_twin_insights": [],
    "last_twin_update": "",
    # AUTONOMOUS COACH
    "last_auto_coach_time": "",
    "auto_coach_log": [],
    # MASTER HEALTH OS
    "last_master_run": "",
    "master_decision_log": [],
    # LONG TERM LEARNING ENGINE
    "long_term_summary": "",
    # 🧠 SELF IMPROVING CORE
    "response_scores": [],
    "prompt_performance": {},
    "active_prompt_style": "balanced",
    "last_learning_update": "",
    "life_os_mode": "auto",
    "user_preferred_mode": "wellness",
    "brain_state": {
    "mode": "wellness",
    "intervention": "normal"
    },
    "burnout_momentum": 0,
    "suppression_state": "none",
    "weight_history": [],
    "daily_health_log": [],
    "daily_food_log": [],
    "engagement_score": 0,
    "risk_forecast": {},
}

def load_memory():
    user = st.session_state.get("user")
    if not user:
        return DEFAULT_MEMORY.copy()

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT data FROM memory WHERE username=?", (user,))
    row = cursor.fetchone()

    if row:
        memory = json.loads(row[0])
    else:
        memory = DEFAULT_MEMORY.copy()

    # ===== Corruption Guard =====
    for key, value in DEFAULT_MEMORY.items():
        if key not in memory:
            memory[key] = value

    if not isinstance(memory.get("master_decision_log"), list):
        memory["master_decision_log"] = []

    if not isinstance(memory.get("mental_history"), list):
        memory["mental_history"] = []

    if not isinstance(memory.get("habit_log"), list):
        memory["habit_log"] = []

    if not isinstance(memory.get("risk_history"), list):
        memory["risk_history"] = []

    memory = validate_memory(memory)
    return memory


def save_memory(memory):  
    user = st.session_state.get("user")
    if not user:
        return

    conn = get_connection()
    cursor = conn.cursor()

    data = json.dumps(memory)

    cursor.execute("""
        INSERT INTO memory (username, data)
        VALUES (?, ?)
        ON CONFLICT(username)
        DO UPDATE SET data=excluded.data
    """, (user, data))

    conn.commit()       

    # ================= MEMORY CORRUPTION GUARD =================

    for key, value in DEFAULT_MEMORY.items():
        if key not in memory:
            memory[key] = value

    # Ensure critical lists are lists
    if not isinstance(memory.get("master_decision_log"), list):
        memory["master_decision_log"] = []

    if not isinstance(memory.get("mental_history"), list):
        memory["mental_history"] = []

    if not isinstance(memory.get("habit_log"), list):
        memory["habit_log"] = []

    if not isinstance(memory.get("risk_history"), list):
        memory["risk_history"] = []

    memory = validate_memory(memory)
    return memory

def validate_memory(memory):
    for key, value in DEFAULT_MEMORY.items():
        if key not in memory:
            memory[key] = value
    return memory

