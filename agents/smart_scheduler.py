import streamlit as st
from datetime import datetime, timedelta
from core.memory import save_memory
from agents.whatsapp_sender import send_whatsapp_message

# --------------------------------------------------
# SHOULD RUN REMINDER CHECK?
# --------------------------------------------------


def should_run_scheduler(memory):

    last = memory.get("last_reminder_check")

    if not last:
        return True

    last_time = datetime.fromisoformat(last)

    # run every 2 hours
    return datetime.now() - last_time > timedelta(hours=2)


# --------------------------------------------------
# GENERATE SMART REMINDERS
# --------------------------------------------------


def generate_reminders(memory):

    reminders = []

    if memory["water_intake"] < 3:
        reminders.append("💧 You may be dehydrated. Drink a glass of water.")

    if memory["energy_level"] <= 3:
        reminders.append("⚡ Energy looks low. Try light stretching.")

    if memory["health_score"] < 40:
        reminders.append("🩺 Health score dropped. Focus on rest and hydration today.")

    if not memory["exercise_done"]:
        reminders.append("🏃 A short walk today can improve your health score.")

    return reminders


# --------------------------------------------------
# MAIN SCHEDULER AGENT
# --------------------------------------------------


def smart_reminder_scheduler(memory):

    if not should_run_scheduler(memory):
        return

    reminders = generate_reminders(memory)

    if reminders:
        st.subheader("⏰ Smart AI Reminders")

        for r in reminders:
            st.warning(r)

    if memory.get("phone_number"):
        send_whatsapp_message(memory["phone_number"], r)

        memory["reminder_log"].extend(reminders)

    memory["last_reminder_check"] = datetime.now().isoformat()
    save_memory(memory)
