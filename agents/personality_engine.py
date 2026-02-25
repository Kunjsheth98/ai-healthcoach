from core.memory import save_memory
import streamlit as st

# -----------------------------------------
# PERSONALITY EVOLUTION ENGINE
# -----------------------------------------

def evolve_personality_from_habits(memory):

    streak = memory.get("streak_days", 0)
    burnout = memory.get("burnout_risk_level", 0)
    engagement = memory.get("engagement_score", 0)

    if burnout >= 7:
        personality = "Calm Recovery Guide"
    elif streak >= 21:
        personality = "High Performance Mentor"
    elif streak >= 7:
        personality = "Structured Accountability Coach"
    elif engagement >= 20:
        personality = "Motivational Growth Coach"
    else:
        personality = "Balanced Guide"

    memory["personality_type"] = personality
    
    save_memory(memory)
# -----------------------------------------
# SHOW PERSONALITY UI
# -----------------------------------------


def personality_display_ui(memory):

    personality = memory.get("personality_type", "adaptive")

    labels = {
        "Calm Recovery Guide": "🧘 Calm Recovery Guide",
        "High Performance Mentor": "🔥 High Performance Mentor",
        "Structured Accountability Coach": "📊 Structured Accountability Coach",
        "Motivational Growth Coach": "🚀 Motivational Growth Coach",
        "Balanced Guide": "⚖ Balanced Guide",
    }

    st.subheader("🧬 Your AI Coach Personality")
    st.info(labels.get(personality, "Adaptive Coach"))


