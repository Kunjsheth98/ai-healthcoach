import streamlit as st


# --------------------------------------------------
# SMART HEALTH NOTIFICATIONS
# --------------------------------------------------

def smart_notification_agent(memory):

    score = memory["health_score"]
    water = memory["water_intake"]
    energy = memory["energy_level"]

    st.subheader("🔔 Smart Health Notifications")

    if water < 3:
        st.warning("💧 Hydration is low today. Try drinking water now.")

    if energy <= 3:
        st.info("⚡ Energy seems low. Consider light stretching or rest.")

    if score < 40:
        st.error(
            "🚨 Health score dropping. Focus on sleep and hydration today."
        )

    if memory.get("exercise_done") is False:
        st.write("🏃 A short 10-minute walk could improve today's score.")
