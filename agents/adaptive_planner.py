import streamlit as st
from datetime import datetime, timedelta
from core.config import client

# --------------------------------------------------
# ANALYZE HABIT DATA
# --------------------------------------------------


def analyze_recent_behavior(memory):

    logs = memory.get("habit_log", [])

    if len(logs) < 3:
        return "Not enough data yet."

    recent = logs[-7:]

    avg_sleep = sum(l["sleep"] for l in recent) / len(recent)
    avg_water = sum(l["water"] for l in recent) / len(recent)
    exercise_days = sum(1 for l in recent if l["exercise"])

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

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": f"""
You are an Indian AI Life Planner.

User Health Score: {memory['health_score']}
Energy Level: {memory['energy_level']}
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
        ],
    )

    st.subheader(f"🧭 Adaptive Plan for {tomorrow}")
    st.success(response.choices[0].message.content)
