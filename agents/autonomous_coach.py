import streamlit as st
from datetime import datetime, timedelta
from core.config import client
from core.memory import save_memory
from agents.whatsapp_sender import send_whatsapp_message
from core.ai_wrapper import call_ai

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

    messages=[
        {
            "role": "system",
            "content": f"""
You are the central AI Health Operating System.

Brain Mode: {memory.get("brain_state", {}).get("mode", "wellness")}
Intervention Level: {memory.get("brain_state", {}).get("intervention", "normal")}

User Data:
Health score: {memory['health_score']}
Energy: {memory['energy_level']}
Sleep: {memory['sleep_hours']}
Water: {memory['water_intake']}
Burnout: {memory.get('burnout_risk_level', 0)}
Streak: {memory['streak_days']}

Instructions:

If Brain Mode = recovery:
- Be calm
- Reduce pressure
- Encourage rest and reset

If Intervention = intensity_reduction:
- Suggest moderate workload
- Encourage balance

If normal:
- Encourage performance and discipline

Give ONE short message.
Under 2 sentences.
Actionable.
Emotionally intelligent.
"""
        }
    ]


    reply = call_ai(memory, messages)
    if not reply:
        reply = "Focus on hydration, sleep and light activity today."


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
        send_whatsapp_message(memory["phone_number"], f"🤖 AI Coach:\n{message}")

    save_memory(memory)
