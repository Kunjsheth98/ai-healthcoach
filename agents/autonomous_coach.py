import streamlit as st
from datetime import datetime, timedelta
from core.config import client
from core.memory import save_memory
from agents.whatsapp_sender import send_whatsapp_message


# --------------------------------------------------
# SHOULD RUN AUTO COACH?
# --------------------------------------------------

def should_run_auto_coach(memory):

    last = memory.get("last_auto_coach_time")

    if not last:
        return True

    last_time = datetime.fromisoformat(last)

    # run every 4 hours
    return datetime.now() - last_time > timedelta(hours=4)


# --------------------------------------------------
# GENERATE COACH MESSAGE
# --------------------------------------------------

def generate_autonomous_message(memory):

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": f"""
You are an autonomous Indian AI Health Coach.

Analyze user state and give ONE short coaching message.

User data:
Health score: {memory['health_score']}
Energy: {memory['energy_level']}
Sleep: {memory['sleep_hours']}
Water: {memory['water_intake']}
Streak: {memory['streak_days']}
Level: {memory['health_level']}

Provide:
- motivation
- small actionable suggestion
- supportive tone
Keep under 2 sentences.
"""
            }
        ],
    )

    return response.choices[0].message.content


# --------------------------------------------------
# MAIN AGENT
# --------------------------------------------------

def autonomous_ai_coach(memory):

    if not should_run_auto_coach(memory):
        return

    message = generate_autonomous_message(memory)

    st.subheader("🤖 Autonomous AI Coach")
    st.info(message)

    memory["auto_coach_log"].append(message)
    memory["last_auto_coach_time"] = datetime.now().isoformat()

    # WhatsApp delivery
    if memory.get("phone_number"):
        send_whatsapp_message(
            memory["phone_number"],
            f"🤖 AI Coach:\n{message}"
        )

    save_memory(memory)
