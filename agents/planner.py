import streamlit as st
from datetime import datetime, timedelta
from core.config import client
from core.ai_wrapper import call_ai
from core.memory import save_memory

def autonomous_planner_agent(memory):
    
    tomorrow = (datetime.now() + timedelta(days=1)).strftime("%A")
    mode = memory.get("life_os_mode", "wellness")


    brain = memory.get("brain_state", {})
    mode = brain.get("mode", "wellness")
    intervention = brain.get("intervention", "normal")
    system_state = memory.get("system_state", "balanced")
    # ===============================
    # Hormonal Planner Influence
    # ===============================

    phase = memory.get("current_cycle_phase")

    if phase == "menstrual":
        memory["cognitive_mode"] = "low_focus"
        planner_intensity = "very_light"

    elif phase == "luteal":
        planner_intensity = "moderate"
    planner_intensity = memory.get("global_intensity_level", "moderate")
    muscle_score = memory.get("muscle_gain_score", 0)
    if muscle_score > 15:
        planner_intensity = "high"

    sleep = memory.get("sleep_hours", 7)
    burnout = memory.get("burnout_risk_level", 0)

    if intervention == "force_recovery":
        planner_intensity = "very light recovery schedule"

    elif intervention == "intensity_reduction":
        planner_intensity = "moderate workload with extra breaks"

    elif mode == "performance":
        if sleep >= 7 and burnout < 60:
            planner_intensity = "high"
        else:
            planner_intensity = "moderate"

    elif mode == "discipline":
        planner_intensity = "strict structured routine"

    elif mode == "resilience":
        planner_intensity = "mental strengthening and balanced day"

    if system_state == "overloaded":
        planner_intensity = "very_light"

    elif system_state == "recovery":
        planner_intensity = "moderate"

    elif system_state == "growth":
        planner_intensity = "high"

    else:
        planner_intensity = "balanced"

    heavy_count = memory.get("heavy_session_count", 0)
    burnout = memory.get("burnout_risk_level", 0)   

    sleep = memory.get("sleep_hours", 7)

    sleep_debt = memory.get("sleep_debt", 0)

    weekday = datetime.now().weekday()

    weekly_split = {
        0: "push",
        1: "pull",
        2: "legs",
        3: "yoga",
        4: "push",
        5: "pull",
        6: "recovery"
    }

    today_split = weekly_split.get(weekday)    

    

    # Cognitive load reduction on leg day
    if today_split == "legs":
        planner_intensity = "moderate"
        memory["cognitive_mode"] = "low_focus"
        save_memory(memory)

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
    if memory.get("cognitive_mode") == "low_focus":
        planner_intensity = "very_light"

    meta = memory.get("meta_strategy")

    if meta == "prioritize_sleep":
        planner_intensity = "very_light"

    elif meta == "reduce_intensity":
        planner_intensity = "moderate"    

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
    Hormonal Stress Index: {memory.get('hormonal_stress_index',0)}
    If Hormonal Stress Index > 75:
    Force recovery-style schedule.
    Reduce cognitive load significantly.
    Planner Intensity Level: {planner_intensity}
    Cognitive Mode: {memory.get("cognitive_mode", "normal")}
    Primary Focus Today: {intent}
    Emotional Archetype: {memory.get('emotional_archetype','unknown')}
    Identity Label: {memory.get('imprint_identity','emerging')}

    Identity Maturity Level: {memory.get("identity_maturity","forming")}

    Strategic Focus: {memory.get("strategic_focus","balanced")}

    If Strategic Focus = recovery:
    Keep day restorative and low pressure.

    If Strategic Focus = performance:
    Structure day around measurable progress.

    If Strategic Focus = calm_regulation:
    Include breathwork, reflection, nervous system reset blocks.

    If Identity Maturity = forming:
    Use supportive tone and low pressure.

    If Identity Maturity = emerging:
    Encourage structured consistency.

    If Identity Maturity = solid:
    Increase accountability and clarity.

    If Identity Maturity = integrated:
    Use confident, high ownership language.

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

    If Cognitive Mode = low_focus:
    Reduce deep work blocks.

    If sleep < 5:
    Reduce cognitive load significantly.
    Encourage early sleep.

    Add more breaks.
    Avoid high decision fatigue tasks.
    Prefer admin / light execution work.

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

    Structure output STRICTLY as:

    Morning:
    - bullet
    - bullet

    Afternoon:
    - bullet
    - bullet

    Evening:
    - bullet
    - bullet

    Do not return paragraphs.
    Only structured bullet sections.

    Keep realistic.
    Indian lifestyle friendly.
    """
            }
    ]
    
    plan = call_ai(memory, messages)
    memory["structured_plan"] = plan
    return memory
