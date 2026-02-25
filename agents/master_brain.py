import streamlit as st
from datetime import datetime, timedelta
from core.memory import save_memory

# import existing agents
from agents.smart_scheduler import smart_reminder_scheduler
from agents.health_risk_predictor import health_risk_predictor
from agents.autonomous_coach import autonomous_ai_coach
from agents.medicine_reminder import medicine_reminder_agent
from core.subscription import has_premium_access
from agents.learning_engine import generate_long_term_summary, should_update_learning
from agents.weekly_story import should_generate_weekly_report, generate_weekly_story
from agents.habit_reinforcement_engine import neural_habit_engine
from agents.neural_consistency_engine import neural_consistency_engine
from agents.identity_lock_engine import identity_lock_system
from agents.user_segmentation import classify_user
# --------------------------------------------------
# SHOULD MASTER RUN?
# --------------------------------------------------


def should_run_master(memory):

    last = memory.get("last_master_run")

    if not last:
        return True

    last_time = datetime.fromisoformat(last)

    # master runs every 2 hours
    return datetime.now() - last_time > timedelta(hours=2)


# --------------------------------------------------
# PRIORITY DECISION ENGINE
# --------------------------------------------------


def decide_actions(memory):

    actions = []

    # Highest priority → medicine
    if memory.get("medicine_schedule"):
        actions.append("medicine")

    # Health danger
    if memory["health_score"] < 40:
        actions.append("risk")

    # Low energy
    if memory["energy_level"] <= 3:
        actions.append("coach")

    # Lifestyle reminders
    if memory["water_intake"] < 3:
        actions.append("reminder")

    return actions


# --------------------------------------------------
# MASTER OS
# --------------------------------------------------


def health_master_brain(memory):

    # ================= STATE VALIDATION =================

    required_keys = [
        "burnout_risk_level",
        "burnout_momentum",
        "energy_level",
        "streak_days",
        "engagement_score"
    ]

    for key in required_keys:
        if key not in memory:
            memory[key] = 0

    # ==============================
    # 1️⃣ CORE SIGNAL EXTRACTION
    # ==============================

    burnout = memory.get("burnout_risk_level", 0)
    momentum = memory.get("burnout_momentum", 0)
    energy = memory.get("energy_level", 5)
    streak = memory.get("streak_days", 0)
    engagement = memory.get("engagement_score", 0)

    # ==============================
    # 2️⃣ WEIGHTED SYSTEM INDEX
    # ==============================

    system_index = (
        (burnout * 0.6) +
        (momentum * 0.2) -
        (energy * 0.1) -
        (streak * 0.05)
    )

    memory["system_index"] = round(system_index, 2)

    # ==============================
    # 3️⃣ STATE CLASSIFICATION
    # ==============================

    if system_index >= 6:
        system_state = "critical_recovery"

    elif system_index >= 3:
        system_state = "preventive_recovery"

    elif energy >= 8 and streak >= 7:
        system_state = "performance_peak"

    else:
        system_state = "stable"

    memory["system_state"] = system_state

    # ==============================
    # 4️⃣ BRAIN MODE DECISION
    # ==============================

    if system_state == "critical_recovery":
        brain_mode = "recovery_lock"
        intervention = "force_recovery"

    elif system_state == "preventive_recovery":
        brain_mode = memory.get("life_os_mode", "wellness")
        intervention = "intensity_reduction"

    elif system_state == "performance_peak":
        brain_mode = "performance"
        intervention = "normal"

    else:
        brain_mode = memory.get("life_os_mode", "wellness")
        intervention = "normal"

    #🔥 GOAL SPECIFIC MODE ENGINE
    goal = memory.get("lifestyle", {}).get("goal", "")

    if goal.lower() in ["fat loss", "weight loss"]:
        memory["goal_mode"] = "fat_loss"

    elif goal.lower() in ["muscle gain", "bulking"]:
        memory["goal_mode"] = "muscle_gain"

    elif goal.lower() in ["stress recovery", "mental reset"]:
        memory["goal_mode"] = "recovery"

    else:
        memory["goal_mode"] = "general"

    memory["brain_state"] = {
        "mode": brain_mode,
        "intervention": intervention
    }

    # ==============================
    # 6️⃣ IDENTITY + HABITS
    # ==============================

    identity = identity_lock_system(memory)
    # 🧬 META IDENTITY REINFORCEMENT

    if memory.get("meta_strategy") == "prioritize_sleep":
        memory["identity_lock"]["current_identity"] = "Recovering Strategist"

    elif memory.get("meta_strategy") == "maintain_path":
        memory["identity_lock"]["current_identity"] = "Strategic Builder"
    neural_habit_engine(memory)
    neural_consistency_engine(memory)
    classify_user(memory)
    adaptive_silence_engine(memory)

    memory.setdefault("master_decision_log", [])
    memory["master_decision_log"].append(
        f"{system_state} | Suppression: {memory.get('suppression_state','none')} | Identity: {identity}"
    )

    # ==============================
    # 7️⃣ LONG TERM LEARNING
    # ==============================

    if should_update_learning(memory):
        generate_long_term_summary(memory)

    # ==============================
    # 8️⃣ WEEKLY STORY
    # ==============================

    if should_generate_weekly_report(memory):
        generate_weekly_story(memory)

    # ==============================
    # 9️⃣ ACTION EXECUTION
    # ==============================

    if not should_run_master(memory):
        save_memory(memory)
        return

    actions = decide_actions(memory)

    for action in actions:

        if action == "medicine" and has_premium_access("smart_scheduler"):
            medicine_reminder_agent(memory)

        elif action == "risk" and has_premium_access("smart_scheduler"):
            health_risk_predictor(memory)

        elif action == "coach" and has_premium_access("smart_scheduler"):
            autonomous_ai_coach(memory)

        elif action == "reminder" and has_premium_access("smart_scheduler"):
            smart_reminder_scheduler(memory)

    memory["last_master_run"] = datetime.now().isoformat()

    memory["daily_insight"] = generate_pattern_insight(memory)    

    try:
        from agents.anticipation_engine import anticipatory_suggestion
        memory["anticipatory_action"] = anticipatory_suggestion(memory)
    except Exception:
        memory["anticipatory_action"] = None

    save_memory(memory)

def adaptive_silence_engine(memory):

    burnout = memory.get("burnout_risk_level", 0)
    engagement = memory.get("usage", {}).get("daily_count", 0)

    if burnout >= 8 and engagement > 20:
        memory["suppression_state"] = "high"
    elif burnout >= 5:
        memory["suppression_state"] = "moderate"
    else:
        memory["suppression_state"] = "none" 

    if memory.get("burnout_risk_level", 0) >= 8:
        memory["life_os_mode"] = "wellness"
        memory["ai_paused"] = False
       

def generate_pattern_insight(memory):
        energy = memory.get("energy_level", 5)
        sleep = memory.get("sleep_hours", 7)
        burnout = memory.get("burnout_risk_level", 0)
        streak = memory.get("streak_days", 0)

        if burnout >= 7:
            return "Your system is under strain. Recovery now prevents breakdown later."
        elif energy < 4 and sleep < 6:
            return "Low sleep is directly affecting your energy."
        elif streak >= 7:
            return "Your consistency is becoming a real identity shift."
        else:
            return "You are stable. Small improvements now compound long term."        