import streamlit as st
from datetime import datetime, timedelta
from core.config import client
from core.memory import save_memory
from core.ai_wrapper import call_ai
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

    pattern_note = ""

    if memory.get("burnout_momentum", 0) > 1:
        pattern_note = "Stress is accelerating compared to earlier in the week."
    elif memory.get("streak_days", 0) >= 7:
        pattern_note = "Consistency has stabilized your system."
    else:
        pattern_note = "Behavior is still forming and adapting."

    memory["behavior_pattern_summary"] = pattern_note

    if len(habits) < 3:
        return
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
    Behavior Pattern Summary: {memory.get('behavior_pattern_summary')}

    Explain:
    - Behavioral pattern observed
    - Risk level
    - Positive reinforcement
    - 1 specific improvement strategy for next week

    Make it intelligent, not generic.
    """
        }
    ]

    story = call_ai(memory, messages)
    if not story:
        story = "This week you showed resilience. Keep going."
        
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
