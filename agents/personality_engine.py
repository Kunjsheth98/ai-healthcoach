from core.memory import save_memory
import streamlit as st

# -----------------------------------------
# PERSONALITY EVOLUTION ENGINE
# -----------------------------------------

def update_personality_identity(memory):

    score = memory["health_score"]
    streak = len(memory["checkin_history"])
    energy = memory["energy_level"]

    personality_score = memory.get("personality_score", 50)

    # gradual evolution
    if score > 70 and streak > 5:
        personality_score += 5

    elif score < 40:
        personality_score -= 5

    # clamp value
    personality_score = max(0, min(100, personality_score))

    memory["personality_score"] = personality_score

    # identity selection
    if personality_score < 30:
        memory["personality_type"] = "supportive_companion"

    elif personality_score < 60:
        memory["personality_type"] = "accountability_partner"

    elif personality_score < 80:
        memory["personality_type"] = "performance_coach"

    else:
        memory["personality_type"] = "elite_trainer"

    save_memory(memory)


# -----------------------------------------
# SHOW PERSONALITY UI
# -----------------------------------------

def personality_display_ui(memory):

    personality = memory.get("personality_type", "adaptive")

    labels = {
        "supportive_companion": "🤍 Supportive Companion",
        "accountability_partner": "🧭 Accountability Partner",
        "performance_coach": "🔥 Performance Coach",
        "elite_trainer": "🚀 Elite Trainer"
    }

    st.subheader("🧬 Your AI Coach Personality")
    st.info(labels.get(personality, "Adaptive Coach"))
