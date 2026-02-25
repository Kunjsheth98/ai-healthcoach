import streamlit as st


def health_risk_agent(memory):

    risks = []

    if memory.get("health_score", 50) < 35:
        risks.append("Low health score")

    if memory.get("sleep_hours", 7) < 5:
        risks.append("Sleep deprivation risk")

    if memory.get("water_intake", 0) < 3:
        risks.append("Dehydration risk")

    if risks:
        st.error("🚨 Health Risk Alerts")
        for r in risks:
            st.write("•", r)
