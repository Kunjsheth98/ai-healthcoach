import streamlit as st

def health_risk_agent(memory):

    risks = []

    if memory["health_score"] < 35:
        risks.append("Low health score")

    if memory["sleep_hours"] < 5:
        risks.append("Sleep deprivation risk")

    if memory["water_intake"] < 3:
        risks.append("Dehydration risk")

    if risks:
        st.error("🚨 Health Risk Alerts")
        for r in risks:
            st.write("•", r)
