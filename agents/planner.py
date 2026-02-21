import streamlit as st
from datetime import datetime, timedelta
from core.config import client


def autonomous_planner_agent(memory):
    brain_mode = memory.get("brain_state", {}).get("mode")

    if brain_mode == "recovery_lock":
        return "⚠ Recovery Mode Activated. Focus on light activity and stress reset."

    if brain_mode == "load_reduction":
        # reduce intensity by 30%
        intensity_modifier = 0.7
    else:
        intensity_modifier = 1
        tomorrow = (datetime.now() + timedelta(days=1)).strftime("%A")

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": f"""
Create a simple Indian health plan.

Health score: {memory['health_score']}
Energy: {memory['energy_level']}
Goal: {memory['health_goals']}
""",
            }
        ],
    )

    st.subheader(f"📅 Tomorrow Plan ({tomorrow})")
    st.success(response.choices[0].message.content)
