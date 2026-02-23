import streamlit as st
from datetime import datetime, timedelta
from core.config import client
from core.memory import save_memory

# --------------------------------------------------
# CHECK IF WEEK PASSED
# --------------------------------------------------


def should_generate_weekly_report(memory):

    last_date = memory.get("weekly_report_date")

    if not last_date:
        return True

    last = datetime.fromisoformat(last_date)
    return datetime.now() - last > timedelta(days=7)

    
# --------------------------------------------------
# GENERATE AI STORY
# --------------------------------------------------


def generate_weekly_story(memory):
    
    habits = memory.get("habit_log", [])

    if len(habits) < 3:
        return

    response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {
            "role": "system",
            "content": f"""
You are an advanced Indian AI Health Coach.

Create a SHORT intelligent weekly behavioral report.

User Data:
Health score: {memory.get('health_score')}
Energy: {memory.get('energy_level')}
Sleep: {memory.get('sleep_hours')}
Water intake: {memory.get('water_intake')}

Mood trend: {memory.get('mood_trend', 'stable')}
Burnout velocity: {memory.get('burnout_velocity', 0)}
Mood volatility index: {memory.get('mood_volatility', 0)}
Sleep-Mood correlation: {memory.get('sleep_mood_correlation', 'weak')}

Explain:
- Behavioral pattern observed
- Risk level
- Positive reinforcement
- 1 specific improvement strategy for next week

Make it intelligent, not generic.
"""
        }
    ],
)

    story = response.choices[0].message.content

    memory["weekly_story"] = story
    memory["weekly_report_date"] = datetime.now().isoformat()
    save_memory(memory)

# --------------------------------------------------
# DISPLAY STORY
# --------------------------------------------------


def weekly_story_ui(memory):

    if should_generate_weekly_report(memory):
        generate_weekly_story(memory)

    story = memory.get("weekly_story")

    if story:
        st.subheader("✨ Your Weekly Health Story")
        st.success(story)
