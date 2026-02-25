import streamlit as st
from datetime import datetime, timedelta
from core.config import client
from core.memory import save_memory
from core.ai_wrapper import call_ai

# --------------------------------------------------
# SHOULD UPDATE TWIN
# --------------------------------------------------


def should_update_twin(memory):

    last = memory.get("last_twin_update")

    if not last:
        return True

    last_time = datetime.fromisoformat(last)

    # update once daily
    return datetime.now() - last_time > timedelta(days=1)


# --------------------------------------------------
# GENERATE PERSONAL INSIGHTS
# --------------------------------------------------


def generate_health_twin(memory):

    logs = memory.get("habit_log", [])

    if len(logs) < 5:
        return

    recent_logs = logs[-10:]

    
    messages=[
        {
            "role": "system",
            "content": f"""
    You are a Personal Health Analysis AI.

    Analyze user's recent health behavior and discover patterns.

    Data:
    {recent_logs}

    Find correlations such as:
    - sleep vs energy
    - hydration vs health score
    - exercise vs mood

    Return 3–5 short personalized insights starting with:
    "Your body responds well when..."
    """,
                }
            ]

    insights_text = call_ai(memory, messages)
    if not insights_text:
        return

    memory["health_twin_insights"] = insights_text.split("\n")
    memory["last_twin_update"] = datetime.now().isoformat()

    save_memory(memory)


# --------------------------------------------------
# UI DISPLAY
# --------------------------------------------------


def health_twin_ui(memory):

    if should_update_twin(memory):
        generate_health_twin(memory)

    insights = memory.get("health_twin_insights")

    if insights:
        st.subheader("🧬 Your Personal Health Twin Insights")

        for i in insights:
            if i.strip():
                st.success(i)
