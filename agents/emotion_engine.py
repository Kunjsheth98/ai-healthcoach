import streamlit as st
from core.memory import save_memory

# -----------------------------------------
# DETECT EMOTIONAL STATE
# -----------------------------------------


def detect_emotional_state(memory):

    score = memory["health_score"]
    energy = memory["energy_level"]
    streak = len(memory["checkin_history"])

    if score < 40 or energy <= 3:
        state = "struggling"

    elif streak >= 5 and score > 65:
        state = "winning"

    elif score > 75:
        state = "challenger"

    else:
        state = "balanced"

    memory["emotional_state"] = state
    save_memory(memory)

    return state


# -----------------------------------------
# SHOW EMOTIONAL FEEDBACK
# -----------------------------------------


def emotional_feedback_ui(memory):

    state = memory.get("emotional_state", "balanced")

    if state == "struggling":
        st.warning(
            "🤍 Your AI Coach Notice: You've had a tough health trend recently. "
            "Let's focus on small achievable wins today."
        )

    elif state == "winning":
        st.success("🔥 Amazing consistency! Your habits are improving steadily.")

    elif state == "challenger":
        st.info("🚀 You're performing very well. Ready to level up your routine?")
