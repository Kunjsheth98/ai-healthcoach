import streamlit as st
from datetime import datetime, timedelta
from core.config import client
from core.memory import save_memory

# --------------------------------------------------
# SHOULD UPDATE LEARNING MEMORY
# --------------------------------------------------


def should_update_learning(memory):

    last = memory.get("last_learning_update")

    if not last:
        return True

    last_time = datetime.fromisoformat(last)

    # update every 3 days
    return datetime.now() - last_time > timedelta(days=3)


# --------------------------------------------------
# GENERATE LONG TERM SUMMARY
# --------------------------------------------------


def generate_long_term_summary(memory):

    logs = memory.get("habit_log", [])

    if len(logs) < 5:
        return

    recent_logs = logs[-20:]  # limit tokens

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": f"""
You are a long-term health learning AI.

Analyze the user's long-term behavior and create a compact
personal health profile summary.

Data:
{recent_logs}

Create a short summary describing:
- lifestyle pattern
- energy behavior
- hydration habits
- exercise consistency
- coaching style preference

Keep under 120 words.
""",
            }
        ],
    )

    summary = response.choices[0].message.content

    memory["long_term_summary"] = summary
    memory["last_learning_update"] = datetime.now().isoformat()

def analyze_mood_trend(memory):

    mood_log = memory.get("emotional_event_log", [])

    if len(mood_log) < 3:
        return

    last_three = [entry["mood"] for entry in mood_log[-3:]]

    if last_three[-1] < last_three[0]:
        mood_trend = "declining"
    elif last_three[-1] > last_three[0]:
        mood_trend = "improving"
    else:
        mood_trend = "stable"

    memory["mood_trend"] = mood_trend    

    save_memory(memory)

    analyze_mood_trend(memory)
# --------------------------------------------------
# UI DISPLAY
# --------------------------------------------------

def learning_engine_ui(memory):

    if should_update_learning(memory):
        generate_long_term_summary(memory)

    if memory.get("long_term_summary"):
        st.subheader("🧠 AI Learned About You")
        st.info(memory["long_term_summary"])
