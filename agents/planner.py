import streamlit as st
from datetime import datetime, timedelta
from core.config import client
from core.ai_wrapper import call_ai

def autonomous_planner_agent(memory):
    
    tomorrow = (datetime.now() + timedelta(days=1)).strftime("%A")
    mode = memory.get("life_os_mode", "wellness")


    brain_mode = memory.get("brain_state", {}).get("mode")


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

    sleep_pattern = memory.get("sleep_pattern", "")
    energy_level = memory.get("energy_level", 5)

    realism_rules = ""
    intent = memory.get("primary_intent", "general") 

    lifestyle = memory.get("lifestyle", {})
    sleep_pattern = lifestyle.get("sleep_pattern", "")
    preferred_wake = lifestyle.get("preferred_wake_time", None)
    energy_level = memory.get("energy_level", 5)

    wake_anchor_rule = ""
    if preferred_wake:
        wake_anchor_rule = f"Anchor the day around wake time: {preferred_wake}. Do not shift drastically."
    if sleep_pattern == "Irregular":
        realism_rules += "Do NOT enforce drastic wake-up time shifts. Stabilize gradually.\n"

    if energy_level <= 4:
        realism_rules += "Avoid high-intensity routines. Keep effort light.\n"

    if intent == "sleep":
        realism_rules += "Primary goal is sleep stabilization, not productivity.\n"

    if intent == "stress":
        realism_rules += "Reduce cognitive overload. Focus on calm structure.\n"    

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
    Primary Focus Today: {intent}

    Intent Rules:
    If intent is "sleep":
    Prioritize sleep stabilization, no drastic wake-up changes.

    If intent is "stress":
    Prioritize recovery, breathing, low cognitive load.

    If intent is "movement":
    Prioritize light physical activation and consistency.

    If intent is "general":
    Follow intensity-based planning.
    Realism Constraints: {realism_rules}
    Wake Anchor:
    {wake_anchor_rule}
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
    
    plan = call_ai(memory, messages)
    if not plan:
        plan = "Focus on hydration, light movement, and 1 key priority tomorrow."
    st.subheader(f"📅 Tomorrow Plan ({tomorrow})")
    st.success(plan)
