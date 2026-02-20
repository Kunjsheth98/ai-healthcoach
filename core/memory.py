import json
import os
import streamlit as st

# =====================================================
# DEFAULT MEMORY STRUCTURE (USER AI BRAIN)
# =====================================================

DEFAULT_MEMORY = {
    "name": "",
    "health_goals": "",
    "phone_number": "",
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
    "last_learning_update": "",
}


def get_memory_path():
    user = st.session_state.get("user")
    if not user:
        return "health_memory.json"
    os.makedirs(f"users/{user}", exist_ok=True)
    return f"users/{user}/memory.json"


def load_memory():
    memory_file = get_memory_path()

    if os.path.exists(memory_file):
        with open(memory_file, "r") as f:
            memory = json.load(f)

        # Auto add new keys
        for key, value in DEFAULT_MEMORY.items():
            if key not in memory:
                memory[key] = value

        return memory

    return DEFAULT_MEMORY.copy()


def save_memory(memory):
    memory_file = get_memory_path()
    with open(memory_file, "w") as f:
        json.dump(memory, f, indent=4)
