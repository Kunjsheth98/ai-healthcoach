from datetime import datetime
from core.memory import save_memory
import streamlit as st

# -----------------------------------------
# STORE DAILY HABIT SNAPSHOT
# -----------------------------------------


def log_daily_habits(memory):

    today = datetime.now().date().isoformat()

    # avoid duplicate logs
    for entry in memory["habit_log"]:
        if entry["date"] == today:
            return

    snapshot = {
        "date": today,
        "sleep": memory["sleep_hours"],
        "water": memory["water_intake"],
        "energy": memory["energy_level"],
        "exercise": memory["exercise_done"],
        "health_score": memory["health_score"],
    }

    memory["habit_log"].append(snapshot)

    # keep last 30 days only
    memory["habit_log"] = memory["habit_log"][-30:]

    save_memory(memory)


# -----------------------------------------
# PATTERN DETECTION
# -----------------------------------------


def analyze_habits(memory):

    logs = memory["habit_log"]

    if len(logs) < 5:
        return "learning"

    avg_sleep = sum(l["sleep"] for l in logs) / len(logs)
    avg_water = sum(l["water"] for l in logs) / len(logs)
    exercise_days = sum(1 for l in logs if l["exercise"])

    insights = []

    if avg_sleep < 6:
        insights.append("You consistently sleep less than recommended.")

    if avg_water < 4:
        insights.append("Hydration habit is below healthy level.")

    if exercise_days < len(logs) * 0.3:
        insights.append("Exercise consistency is low.")

    return insights


# -----------------------------------------
# PERSONALITY ADAPTATION
# -----------------------------------------


def update_personality(memory):

    score = memory["health_score"]

    if score < 40:
        memory["personality_mode"] = "supportive"

    elif score > 75:
        memory["personality_mode"] = "challenger"

    else:
        memory["personality_mode"] = "balanced"

    save_memory(memory)


# -----------------------------------------
# SHOW HABIT INSIGHTS
# -----------------------------------------


def habit_insight_ui(memory):

    insights = analyze_habits(memory)

    if insights == "learning":
        st.info("🧠 AI is learning your habits...")
        return

    if insights:
        st.subheader("🧠 Habit Insights")
        for i in insights:
            st.write("•", i)
