import streamlit as st
from datetime import datetime, timedelta
from core.memory import save_memory

# --------------------------------------------------
# SHOULD RUN RISK ANALYSIS
# --------------------------------------------------


def should_run_risk_check(memory):

    last = memory.get("last_risk_check")

    if not last:
        return True

    last_time = datetime.fromisoformat(last)

    # run every 6 hours
    return datetime.now() - last_time > timedelta(hours=6)


# --------------------------------------------------
# ANALYZE HEALTH PATTERNS
# --------------------------------------------------


def analyze_health_risks(memory):

    risks = []

    sleep = memory.get("sleep_hours", 6)
    energy = memory.get("energy_level", 5)
    water = memory.get("water_intake", 0)
    score = memory.get("health_score", 50)
    streak = memory.get("streak_days", 0)

    if sleep < 5:
        risks.append("😴 Sleep has been low. Fatigue or burnout risk may increase.")

    if water < 3:
        risks.append("💧 Hydration trend is low. Possible dehydration risk.")

    if energy <= 3:
        risks.append("⚡ Low energy detected. Consider rest and light activity.")

    if score < 40:
        risks.append("🩺 Health score declining. Lifestyle imbalance risk.")

    if streak == 0:
        risks.append("📉 Routine inconsistency detected. Habit loss risk.")

    return risks


# --------------------------------------------------
# MAIN RISK AGENT
# --------------------------------------------------


def health_risk_predictor(memory):

    if not should_run_risk_check(memory):
        return

    risks = analyze_health_risks(memory)

    if risks:

        st.subheader("🧠 AI Health Risk Insights")

        for r in risks:
            st.error(r)

        memory.setdefault("risk_history", [])
        memory["risk_history"].extend(risks)

    memory["last_risk_check"] = datetime.now().isoformat()
    save_memory(memory)
