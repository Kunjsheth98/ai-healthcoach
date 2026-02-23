import streamlit as st
from core.config import client

# ---------------------------------------------------
# DETERMINE WORKOUT TYPE
# ---------------------------------------------------


def choose_movement_type(memory):
    brain = memory.get("brain_state", {})
    intervention = brain.get("intervention")

    suppression = memory.get("suppression_state", "none")

    if suppression == "high":
        return "recovery"

    if intervention == "force_recovery":
        return "recovery"
    
    energy = memory["energy_level"]
    sleep = memory["sleep_hours"]
    exercised = memory["exercise_done"]

    # Recovery condition
    if sleep < 5:
        return "recovery"

    if energy <= 3:
        return "yoga"

    if energy <= 6:
        return "light_workout"

    if exercised:
        return "stretching"

    return "strength"


# ---------------------------------------------------
# GENERATE AI MOVEMENT PLAN
# ---------------------------------------------------


def movement_coach_agent(memory):

    mode = memory.get("life_os_mode", "wellness")

    brain = memory.get("brain_state", {})
    intervention = brain.get("intervention", "normal")

    # Header always shown
    st.subheader("🧘 Exercise & Yoga Coach")

    if intervention == "force_recovery":
        st.warning("⚠ Recovery Mode Activated by AI Brain")
    elif intervention == "intensity_reduction":
        st.info("⚠ Reduced Intensity Mode Activated")
    elif mode == "performance":
        st.success("🔥 High Performance Mode")
    elif mode == "discipline":
        st.success("💪 Structured Discipline Mode")
    elif mode == "resilience":
        st.info("🧘 Emotional Resilience Focus")
    elif mode == "wellness":
        st.info("🌿 Balanced Wellness Mode")
    
    movement_type = choose_movement_type(memory)
    prompts = {
        "recovery": "Create a gentle recovery routine with breathing and stretching.",
        "yoga": "Create a beginner-friendly Indian yoga session (15 minutes).",
        "light_workout": "Create a simple home workout without equipment (20 minutes).",
        "strength": "Create a strength-focused bodyweight workout.",
        "stretching": "Create a relaxing stretching routine for recovery.",

    }
    if movement_type == "recovery":
        st.success("Gentle stretching + breathing 15 mins.")
        return
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": f"""
You are an Indian AI Movement Coach.

Life Mode: {mode}
Brain Intervention: {intervention}
Burnout Risk: {memory.get('burnout_risk_level',0)}

User stats:
Health score: {memory['health_score']}
Energy level: {memory['energy_level']}
Sleep hours: {memory['sleep_hours']}

Movement Type: {movement_type}

If Brain Intervention = force_recovery:
Keep routine very light and calming.

If Brain Intervention = intensity_reduction:
Reduce normal intensity by 30%.

{prompts[movement_type]}

Provide:
- warmup
- main exercises/yoga poses
- duration
- safety advice

Keep beginner friendly and realistic.
""",
            }
        ],
    )

    plan = response.choices[0].message.content

    st.subheader("🧘 Exercise & Yoga Coach")
    st.success(plan)
