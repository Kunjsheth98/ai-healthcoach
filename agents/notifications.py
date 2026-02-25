import streamlit as st

def notification_logic_agent(memory):

    messages = []

    water = memory.get("water_intake", 0)
    score = memory.get("health_score", 50)

    if water < 4:
        messages.append("Drink more water 💧")

    if score < 50:
        messages.append("Your health score dropped.")

    if messages:
        st.info("🔔 Smart Notifications")
        for m in messages:
            st.write("•", m)