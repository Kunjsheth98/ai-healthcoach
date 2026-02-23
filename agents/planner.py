import streamlit as st
from datetime import datetime, timedelta
from core.config import client


def autonomous_planner_agent(memory):

    mode = memory.get("life_os_mode", "wellness")

    if mode == "performance":
        return "🔥 Performance Plan: Aggressive goal focus tomorrow."

    elif mode == "discipline":
        return "📅 Discipline Plan: Strict structured routine."

    elif mode == "resilience":
        return "🧘 Resilience Plan: Reduced workload + mental recovery."

    elif mode == "wellness":
        return "🌿 Wellness Plan: Balanced productivity + rest."

    brain_mode = memory.get("brain_state", {}).get("mode")

    if brain_mode == "recovery_lock":
        return "⚠ Recovery Mode Activated. Focus on light activity and stress reset."

    if brain_mode == "load_reduction":
        # reduce intensity by 30%
        intensity_modifier = 0.7
    else:
        intensity_modifier = 1
        tomorrow = (datetime.now() + timedelta(days=1)).strftime("%A")


    brain = memory.get("brain_state", {})
    mode = brain.get("mode", "wellness")
    intervention = brain.get("intervention", "normal")

    planner_intensity = "balanced"

    if intervention == "force_recovery":
        planner_intensity = "very light recovery schedule"

    elif intervention == "intensity_reduction":
        planner_intensity = "moderate workload with extra breaks"

    elif mode == "performance":
        planner_intensity = "high productivity structured day"

    elif mode == "discipline":
        planner_intensity = "strict structured routine"

    elif mode == "resilience":
        planner_intensity = "mental strengthening and balanced day"

    burnout = memory.get("burnout_risk_level", 0)
    momentum = memory.get("burnout_momentum", 0)
    energy = memory.get("energy_level", 5)

    intensity_score = energy - burnout - momentum

    if intensity_score <= 2:
        planner_intensity = "very_light"
    elif intensity_score <= 4:
        planner_intensity = "moderate"
    else:
        planner_intensity = "high"

    suppression = memory.get("suppression_state", "none")

    if suppression == "high":
        planner_intensity = "very_light"

    response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {
            "role": "system",
            "content": f"""
You are Asha — an AI Life OS Planner.

User State:
Health Score: {memory.get('health_score',50)}
Energy Level: {memory.get('energy_level',5)}
Life Mode: {memory.get('life_os_mode','wellness')}
Brain Mode: {memory.get('brain_state',{}).get('mode')}
Intervention: {memory.get('brain_state',{}).get('intervention')}
Burnout Risk: {memory.get('burnout_risk_level',0)}
Planner Intensity Level: {planner_intensity}
Instructions:
If Planner Intensity Level = very_light:
Create recovery focused day.

If moderate:
Create balanced day.

If high:
Create high productivity structured day.

If Intervention = force_recovery:
Create very light recovery day.

If Intervention = intensity_reduction:
Create structured day with 30% reduced workload.

If Life Mode = performance:
Make day goal-driven.

If Life Mode = discipline:
Make day strict and structured.

If Life Mode = resilience:
Include mental reset blocks.

If Life Mode = wellness:
Balanced day.

Structure output as:

Morning:
Afternoon:
Evening:

Keep realistic.
Indian lifestyle friendly.
"""
        }
    ]
)
    st.subheader(f"📅 Tomorrow Plan ({tomorrow})")
    st.success(response.choices[0].message.content)
