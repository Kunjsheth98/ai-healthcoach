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

    return insights


# --------------------------------------------------
# ADAPTIVE LIFE PLAN
# --------------------------------------------------


def adaptive_life_planner(memory):

    insights = analyze_recent_behavior(memory)

    tomorrow = (datetime.now() + timedelta(days=1)).strftime("%A")

    
    messages=[
        {
            "role": "system",
            "content": f"""
    You are an Indian AI Life Planner.

    User Health Score: {memory['health_score']}
    Energy Level: {memory['energy_level']}
    Brain Mode: {memory.get('brain_state',{}).get('mode','wellness')}
    Intervention: {memory.get('brain_state',{}).get('intervention','normal')}
    Burnout Risk: {memory.get('burnout_risk_level',0)}
    Goal: {memory.get('health_goals','fitness')}

    Recent habit insights:
    {insights}

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
        plan = "Focus on hydration, 7 hours sleep, and 20 minutes walking tomorrow"

    st.subheader(f"🧭 Adaptive Plan for {tomorrow}")
    st.success(plan)
