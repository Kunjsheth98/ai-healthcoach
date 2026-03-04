import streamlit as st
from datetime import datetime, timedelta
from core.config import client
from core.ai_wrapper import call_ai
# --------------------------------------------------
# ANALYZE HABIT DATA
# --------------------------------------------------


def analyze_recent_behavior(memory):

    logs = memory.get("habit_log", [])

    if len(logs) < 3:
        return "Not enough data yet."

    recent = logs[-7:]

    avg_sleep = sum(l.get("sleep", 6) for l in recent) / len(recent)
    avg_water = sum(l.get("water", 0) for l in recent) / len(recent)
    exercise_days = sum(1 for l in recent if l.get("exercise", False))

    insights = []

    if avg_sleep < 6:
        insights.append("Improve sleep duration")

    if avg_water < 4:
        insights.append("Increase hydration")

    if exercise_days < 3:
        insights.append("Increase exercise consistency")

    if not insights:
        insights.append("Maintain current healthy routine")

    return ", ".join(insights)


# --------------------------------------------------
# ADAPTIVE LIFE PLAN
# --------------------------------------------------

def adaptive_life_planner(memory):

    fix_sleep = memory.get("fix_sleep_cycle", False)
    preferred_wake = memory.get("lifestyle", {}).get("preferred_wake_time")

    sleep_rule = ""

    if fix_sleep:
        sleep_rule = """
    Gradually improve the user's sleep cycle.
    Do NOT drastically change wake time.

    Adjust wake time by 30–60 minutes earlier each day until healthy.
    Recommend earlier sleep accordingly.
    """
    else:
        sleep_rule = """
    Do not change the user's natural wake time.
    Build the schedule around their current routine.
    """

    insights = analyze_recent_behavior(memory)

    tomorrow = (datetime.now() + timedelta(days=1)).strftime("%A")

    sleep_time = memory.get("sleep_time")
    messages=[
        {
            "role": "system",
            "content": f"""
    You are an Indian AI Life Planner.
    
    User Health Score: {memory.get('health_score', 50)}
    Energy Level: {memory.get('energy_level', 5)}
    Brain Mode: {memory.get('brain_state',{}).get('mode','wellness')}
    Intervention: {memory.get('brain_state',{}).get('intervention','normal')}
    Burnout Risk: {memory.get('burnout_risk_level',0)}
    Goal: {memory.get('health_goals','fitness')}

    User Wake Preference: {preferred_wake}
    User Sleep Preference: {sleep_time}
    Sleep Strategy:
    {sleep_rule}

    Recent habit insights:
    {insights}

    IMPORTANT RULES:
    - If sleep correction is enabled, gradually move wake time earlier (30–60 minutes).
        Otherwise respect user's preferred wake time.
    - Keep the schedule aligned with the user's natural sleep cycle.
    - If wake time is late (example: 12 PM), adjust meals and exercise accordingly.

    Create a personalized DAILY ROUTINE for tomorrow including:
    - wake-up suggestion
    - meals
    - hydration plan
    - exercise suggestion
    - sleep timing

    Keep it simple, motivating and realistic.
    """,
                }
            ]

    plan = call_ai(memory, messages)
    if not plan:
        plan = """
            Morning:
            - Drink water after waking
            - Light stretching

            Afternoon:
            - Balanced lunch
            - 10 minute walk

            Evening:
            - Light dinner
            - Sleep early
            """

    st.subheader(f"🧭 Adaptive Plan for {tomorrow}")
    st.success(plan)
