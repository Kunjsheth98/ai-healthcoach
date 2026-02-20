import streamlit as st


def notification_logic_agent(memory):

    messages = []

    if memory["water_intake"] < 4:
        messages.append("Drink more water 💧")

    if memory["health_score"] < 50:
        messages.append("Your health score dropped.")

    if messages:
        st.info("🔔 Smart Notifications")
        for m in messages:
            st.write("•", m)
