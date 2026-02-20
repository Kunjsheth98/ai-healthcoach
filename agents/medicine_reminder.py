import streamlit as st
from datetime import datetime, timedelta
from core.memory import save_memory
from agents.whatsapp_sender import send_whatsapp_message

# --------------------------------------------------
# CREATE REMINDER SCHEDULE FROM MEDICINES
# --------------------------------------------------


def generate_medicine_schedule(memory):

    if not memory.get("medicines"):
        return

    schedule = []

    for entry in memory["medicines"]:

        lines = entry.split("\n")

        for line in lines:

            text = line.lower()

            if "morning" in text:
                schedule.append({"medicine": line, "time": "09:00"})

            if "afternoon" in text:
                schedule.append({"medicine": line, "time": "14:00"})

            if "night" in text or "evening" in text:
                schedule.append({"medicine": line, "time": "21:00"})

    memory["medicine_schedule"] = schedule
    save_memory(memory)


# --------------------------------------------------
# SHOULD CHECK NOW
# --------------------------------------------------


def should_check_medicine(memory):

    last = memory.get("last_medicine_check")

    if not last:
        return True

    last_time = datetime.fromisoformat(last)

    return datetime.now() - last_time > timedelta(minutes=30)


# --------------------------------------------------
# CHECK REMINDERS
# --------------------------------------------------


def medicine_reminder_agent(memory):

    if not should_check_medicine(memory):
        return

    now = datetime.now().strftime("%H:%M")

    reminders = []

    for item in memory.get("medicine_schedule", []):
        if item["time"] == now:
            reminders.append(item["medicine"])

    if reminders:

        st.subheader("💊 Medicine Reminder")

        for r in reminders:
            message = f"⏰ Time to take your medicine:\n{r}"

            st.warning(message)

            if memory.get("phone_number"):
                send_whatsapp_message(memory["phone_number"], message)

    memory["last_medicine_check"] = datetime.now().isoformat()
    save_memory(memory)
