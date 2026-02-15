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
You are a friendly Indian AI Health Coach.

Create a SHORT motivational weekly health story.

User stats:
Health score: {memory['health_score']}
Energy: {memory['energy_level']}
Sleep: {memory['sleep_hours']}
Water intake: {memory['water_intake']}

Explain:
- improvement
- concern areas
- encouragement for next week

Write emotionally and positively.
"""
            }
        ]
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
