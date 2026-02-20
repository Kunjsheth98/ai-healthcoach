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
    # ---- Long-Term Learning Update ----
    if should_update_learning(memory):
        generate_long_term_summary(memory)

    if not should_run_master(memory):
        return

    st.subheader("🧠 Health Operating System")

    actions = decide_actions(memory)

    if not actions:
        st.success("System stable ✅")
    else:

        for action in actions:

            # ---------------- MEDICINE (PREMIUM) ----------------
            if action == "medicine":
                if has_premium_access("smart_scheduler"):
                    medicine_reminder_agent(memory)

            # ---------------- RISK PREDICTION (PREMIUM) ----------
            elif action == "risk":
                if has_premium_access("smart_scheduler"):
                    health_risk_predictor(memory)
                else:
                    st.info("🔒 Risk prediction is Premium")

            # ---------------- AUTONOMOUS COACH (PREMIUM) --------
            elif action == "coach":
                if has_premium_access("smart_scheduler"):
                    autonomous_ai_coach(memory)
                else:
                    st.info("🔒 Autonomous coaching is Premium")

            # ---------------- SMART REMINDERS -------------------
            elif action == "reminder":
                if has_premium_access("smart_scheduler"):
                    smart_reminder_scheduler(memory)
                else:
                    st.info("🔒 Smart reminders are Premium")

    memory["master_decision_log"].append(
        f"Run at {datetime.now().isoformat()} → {actions}"
    )

    memory["last_master_run"] = datetime.now().isoformat()

    save_memory(memory)
