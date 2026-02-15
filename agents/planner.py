import streamlit as st
from datetime import datetime, timedelta
from core.config import client

def autonomous_planner_agent(memory):

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
"""
            }
        ]
    )

    st.subheader(f"📅 Tomorrow Plan ({tomorrow})")
    st.success(response.choices[0].message.content)
