import streamlit as st
from core.config import client

# ---------------------------------------------------
# DETERMINE WORKOUT TYPE
# ---------------------------------------------------


def choose_movement_type(memory):

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

    if mode == "performance":
        st.subheader("🧘 Exercise & Yoga Coach")
        st.success("🔥 High Performance Workout Mode Activated.")
        # continue normal logic

    elif mode == "discipline":
        st.subheader("🧘 Exercise & Yoga Coach")
        st.success("💪 Structured Discipline Training Activated.")
        # continue normal logic

    elif mode == "resilience":
        st.subheader("🧘 Exercise & Yoga Coach")
        st.info("🧘 Emotional Resilience Session Recommended.")
        st.success("Light yoga + breathing session.")
        return

    elif mode == "wellness":
        st.subheader("🧘 Exercise & Yoga Coach")
        st.info("🌿 Wellness Recovery Session.")
        st.success("Gentle stretching and mobility today.")
        return

    # ================= CENTRAL BRAIN OVERRIDE =================
    brain_mode = memory.get("brain_state", {}).get("mode")

    if brain_mode == "recovery_lock":
        st.subheader("🧘 Exercise & Yoga Coach")
        st.warning("⚠ Recovery Mode Activated by AI Brain")
        st.success("Today focus on deep breathing, light stretching and 20 min slow walk.")
        return

    if brain_mode == "load_reduction":
        st.subheader("🧘 Exercise & Yoga Coach")
        st.info("⚠ Reduced Intensity Mode Activated")
        st.success("Do 15 min light yoga or mobility. Avoid heavy workouts today.")
        return
    
    movement_type = choose_movement_type(memory)

    prompts = {
        "recovery": "Create a gentle recovery routine with breathing and stretching.",
        "yoga": "Create a beginner-friendly Indian yoga session (15 minutes).",
        "light_workout": "Create a simple home workout without equipment (20 minutes).",
        "strength": "Create a strength-focused bodyweight workout.",
        "stretching": "Create a relaxing stretching routine for recovery.",
    }

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": f"""
You are an Indian fitness and yoga coach.

User stats:
Health score: {memory['health_score']}
Energy level: {memory['energy_level']}
Sleep hours: {memory['sleep_hours']}

{prompts[movement_type]}

Provide:
- warmup
- main exercises/yoga poses
- duration
- safety advice

Keep it beginner friendly and realistic.
""",
            }
        ],
    )

    plan = response.choices[0].message.content

    st.subheader("🧘 Exercise & Yoga Coach")
    st.success(plan)
