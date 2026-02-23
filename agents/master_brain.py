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
from agents.weekly_story import generate_weekly_story
from agents.neural_consistency_engine import neural_consistency_engine
from agents.identity_lock_engine import identity_lock_system
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

    # ================================
    # NEURAL PRIORITY EVALUATION
    # ================================

    burnout = memory.get("burnout_risk_level", 0)
    momentum = memory.get("burnout_momentum", 0)
    energy = memory.get("energy_level", 5)
    streak = memory.get("streak_days", 0)

    system_state = "stable"

    if burnout >= 8:
        system_state = "critical_recovery"
    elif burnout >= 5 or momentum > 2:
        system_state = "preventive_recovery"
    elif energy >= 8 and streak >= 7:
        system_state = "performance_peak"

    memory["system_state"] = system_state

    # ================================
    # APPLY BRAIN MODE
    # ================================

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

    memory["brain_state"] = {
        "mode": brain_mode,
        "intervention": intervention
    }

    # ================================
    # SUPPRESSION
    # ================================
    burnout = memory.get("burnout_risk_level", 0)
    engagement = memory.get("engagement_score", 0)
    last_message_depth = memory.get("last_message_depth", 0)

    if burnout >= 8 and engagement < 5:
        memory["suppression_state"] = "high"

    elif burnout >= 5:
        memory["suppression_state"] = "moderate"

    elif last_message_depth > 7:
        memory["suppression_state"] = "low"

    else:
        memory["suppression_state"] = "none"

    # ================================
    # IDENTITY + HABITS + CONSISTENCY
    # ================================

    identity = identity_lock_system(memory)
    neural_habit_engine(memory)
    neural_consistency_engine(memory)

    memory["master_decision_log"].append(
        f"System State: {system_state} | Identity: {identity}"
    )

    # ================================
    # LONG TERM LEARNING
    # ================================

    if should_update_learning(memory):
        generate_long_term_summary(memory)

    # ================================
    # WEEKLY STORY
    # ================================

    if should_generate_weekly_report(memory):
        generate_weekly_story(memory)

    # ================================
    # ACTION EXECUTION
    # ================================

    if not should_run_master(memory):
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

    save_memory(memory)