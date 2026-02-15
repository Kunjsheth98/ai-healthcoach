import streamlit as st
from datetime import datetime
from core.config import client
from core.memory import save_memory
from agents.whatsapp_sender import send_whatsapp_message



# --------------------------------------------------
# SHOULD GENERATE NEW BRIEFING?
# --------------------------------------------------

def should_generate_briefing(memory):

    today = datetime.now().date().isoformat()

    return memory.get("last_briefing_date") != today


# --------------------------------------------------
# GENERATE AI BRIEFING
# --------------------------------------------------

def generate_morning_briefing(memory):

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": f"""
You are a friendly Indian AI Health Coach.

Create a SHORT morning health briefing.

User stats:
Health score: {memory['health_score']}
Energy: {memory['energy_level']}
Sleep hours: {memory['sleep_hours']}
Water intake: {memory['water_intake']}
Streak: {memory['streak_days']} days
Health Level: {memory['health_level']}

Include:
- greeting
- today's focus
- motivation
- simple achievable goal

Keep it concise and encouraging.
"""
            }
        ]
    )

    briefing = response.choices[0].message.content

    memory["morning_briefing"] = briefing
    memory["last_briefing_date"] = datetime.now().date().isoformat()

    save_memory(memory)

    if memory.get("phone_number"):
        send_whatsapp_message(
            memory["phone_number"],
            f"🌅 Morning Health Briefing:\n\n{briefing}"
        )

# --------------------------------------------------
# DISPLAY BRIEFING
# --------------------------------------------------

def morning_briefing_ui(memory):

    if should_generate_briefing(memory):
        generate_morning_briefing(memory)

    briefing = memory.get("morning_briefing")

    if briefing:
        st.subheader("🌅 Your AI Morning Briefing")
        st.success(briefing)
