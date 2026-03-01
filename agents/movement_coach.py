import streamlit as st
from core.config import client
from core.ai_wrapper import call_ai
from core.memory import save_memory
from datetime import datetime
# ---------------------------------------------------
# DETERMINE WORKOUT TYPE
# ---------------------------------------------------

def choose_movement_type(memory):

    weekly_split = {
        0: "push",
        1: "pull",
        2: "legs",
        3: "yoga",
        4: "push",
        5: "pull",
        6: "recovery"
    }

    today = datetime.now()
    weekday = today.weekday()  # 6 = Sunday

    # Weekly reset on Sunday
    if weekday == 6 and memory.get("heavy_session_count", 0) != 0:
        memory["heavy_session_count"] = 0
        save_memory(memory)

    split_type = weekly_split.get(weekday)
    # ===============================
    # Hormonal Movement Override
    # ===============================

    phase = memory.get("current_cycle_phase")

    if phase == "menstrual":
        return "recovery"

    elif phase == "luteal":
        if memory.get("energy_level", 5) <= 6:
            return "light_workout"
    brain = memory.get("brain_state", {})
    meta = memory.get("meta_strategy")

    if meta == "prioritize_sleep":
        return "recovery"

    elif meta == "reduce_intensity":
        return "light_workout"
    global_intensity = memory.get("global_intensity_level", "moderate")
    intervention = brain.get("intervention")

    system_state = memory.get("system_state", "balanced")

    if system_state == "overloaded":
        return "recovery"

    if system_state == "recovery":
        return "yoga"

    if system_state == "growth":
        return "strength"

    if intervention == "force_recovery":
        return "recovery"
    
    energy = memory["energy_level"]
    sleep = memory["sleep_hours"]
    exercised = memory.get("exercise_done", False)

    # Recovery condition

    if energy <= 3:
        return "yoga"
    
    if memory.get("burnout_risk_level", 0) >= 8:
        return "recovery"

    sleep_debt = memory.get("sleep_debt", 0)

    # Severe accumulated debt → force recovery
    if sleep_debt > 40:
        return "recovery"

    # Moderate debt → downgrade intensity
    elif sleep_debt > 25:
        return "yoga"    
    if global_intensity == "very_light":
        return "recovery"
        
    # Default movement type
    if energy <= 6:
        movement_type = "light_workout"
    elif exercised:
        movement_type = "stretching"
    else:
        movement_type = split_type if split_type else "strength"

    # Sleep-based workout adjustment
    if sleep < 5:
        return "recovery"

    elif sleep < 6:
        return "yoga"

    elif sleep < 7:
        movement_type = "light_workout"    

    # --- Progression Upgrade ---
    progression = memory.get("consistency_score", 0)
    muscle_score = memory.get("muscle_gain_score", 0)
    if muscle_score > 10 and movement_type in ["strength", "push", "pull", "legs"]:
        movement_type = "advanced_strength"
    heavy_count = memory.get("heavy_session_count", 0)

    # Gradual decay if user is doing lighter sessions
    if movement_type in ["yoga", "light_workout", "stretching"]:
        memory["heavy_session_count"] = max(0, heavy_count - 1)
        save_memory(memory)
    
    if progression >= 10 and movement_type == "strength":
        return "advanced_strength"

    if progression >= 5 and movement_type == "light_workout":
        return "strength"
    if progression >= 8 and movement_type == "yoga":
        return "advanced_yoga"

    heavy_count = memory.get("heavy_session_count", 0)
    burnout = memory.get("burnout_risk_level", 0)

    bf_trend = memory.get("body_fat_trend_7d", 0)

    # If gaining fat too fast → reduce intensity
    if bf_trend > 0.5:
        return "light_workout"

    # If cutting successfully → allow progression
    if bf_trend < -0.3 and progression > 5:
        return "strength"


    # If too many heavy sessions in a row → force lighter training
    if heavy_count >= 4 or burnout >= 8:
        return "recovery"
    return movement_type


# ---------------------------------------------------
# GENERATE AI MOVEMENT PLAN
# ---------------------------------------------------


def movement_coach_agent(memory):

    mode = memory.get("life_os_mode", "wellness")
    brain = memory.get("brain_state", {})
    intervention = brain.get("intervention", "normal")

    movement_type = choose_movement_type(memory)
    memory["movement_plan_type"] = movement_type

    if memory.get("consistency_score", 0) == 0:
        st.info("🟢 Beginner Mode: Start slow. Focus on form over intensity.")
    prompts = {
        "recovery": "Create a 15-minute nervous system reset session.",
        "yoga": "Create a beginner-friendly Indian yoga flow (15-20 min).",
        "light_workout": "Create a simple home workout without equipment (20 min).",
        "strength": "Create a strength-focused bodyweight workout (25 min).",
        "stretching": "Create a relaxing stretching routine (15 min).",
        "advanced_strength": "Create an advanced bodyweight workout (30 min, progressive overload).",
        "push": "Create a Push workout (chest, shoulders, triceps).",
        "pull": "Create a Pull workout (back, biceps).",
        "legs": "Create a Leg day workout (quads, hamstrings, glutes).",
        "advanced_yoga": "Create an intermediate yoga flow with balance and strength poses (25 min)."
    }

    messages = [
        {
            "role": "system",
            "content": f"""
    You are an elite Indian AI Movement Coach.

    User Profile:
    Energy Level: {memory.get('energy_level',5)}
    Sleep Hours: {memory.get('sleep_hours',0)}
    Health Score: {memory.get('health_score',50)}
    Burnout Risk: {memory.get('burnout_risk_level',0)}
    Life Mode: {mode}
    Identity: {memory.get('imprint_identity','emerging')}
    Archetype: {memory.get('emotional_archetype','neutral')}

    Identity Maturity Level: {memory.get("identity_maturity","forming")}

    Strategic Focus: {memory.get("strategic_focus","balanced")}

    If Strategic Focus = recovery:
    Avoid heavy training.

    If Strategic Focus = performance:
    Emphasize progression and measurable effort.

    If Strategic Focus = calm_regulation:
    Favor yoga, mobility, breathing.

    If Identity Maturity = forming:
    Keep instructions simple and confidence-building.

    If Identity Maturity = emerging:
    Encourage consistency and clean execution.

    If Identity Maturity = solid:
    Increase structure and progression emphasis.

    If Identity Maturity = integrated:
    Use strong performance language and progressive overload focus.

    If Archetype = overloaded:
    Keep tone calm and restorative.

    If Archetype = achiever:
    Encourage structured progression.

    If Archetype = self_critical:
    Avoid shame language.
    Brain Intervention: {intervention}
    Consistency Score: {memory.get('consistency_score',0)}
    Selected Movement Type: {movement_type}
    Movement Instruction:
    {prompts.get(movement_type, "")}
    Hormonal Stress Index: {memory.get('hormonal_stress_index',0)}
    If Hormonal Stress Index > 75:
    Reduce volume by 40%.
    Avoid heavy compound movements.

    Intensity Rules:
    If Brain Intervention = force_recovery → Make session extremely light.
    If Brain Intervention = intensity_reduction → Reduce volume by 30%.
    If Burnout Risk > 70 → Prioritize nervous system reset.
    If Energy <= 3 → Keep session calm and short.

    STRICT OUTPUT FORMAT:

    Session Title:
    Total Duration:

    Step-by-step Instructions:

    1. Warmup (exact exercises + reps or time)
    2. Main Block (clear sets, reps, rest time)
    3. Cooldown (specific stretches or breathing)
    4. Safety Advice (short and practical)

    Make it:
    - Beginner-friendly
    - Home-friendly
    - Indian lifestyle realistic
    - Clear and actionable
    - No fluff
    """
        }
    ]

    # Only generate if not already generated today
    today = str(datetime.now().date())

    if memory.get("movement_plan_date") != today:
        plan = call_ai(memory, messages)

        if not plan:
            plan = "15 min brisk walking + 5 min stretching."

        memory["movement_plan"] = plan
        memory["movement_plan_date"] = today
        save_memory(memory)
    else:
        plan = memory.get("movement_plan")

    st.success(plan)

    today = str(datetime.now().date())
    # --- Passive Recovery Decay (No Workout Logged Today) ---
    last_workout = memory.get("last_workout_date")
    heavy_count = memory.get("heavy_session_count", 0)

    last_decay = memory.get("last_heavy_decay_date")
    if last_workout != today and heavy_count > 0 and last_decay != today:
        memory["heavy_session_count"] = heavy_count - 1
        memory["last_heavy_decay_date"] = today
        save_memory(memory)

    if memory.get("last_workout_date") == today:
        st.info("Workout already logged today.")
    elif st.button("✅ Mark Workout Completed"):
        memory["exercise_done"] = True
        memory["last_workout_date"] = today
        memory["consistency_score"] = memory.get("consistency_score", 0) + 1

        movement_type = memory.get("movement_plan_type")
        sleep = memory.get("sleep_hours", 7)

        burnout = memory.get("burnout_risk_level", 0)
        heavy_count = memory.get("heavy_session_count", 0)

        # 🔁 Recovery day resets load & reduces burnout
        if movement_type == "recovery":
            memory["heavy_session_count"] = 0
            burnout = max(0, burnout - 15)

        # 💪 Heavy session increases load + burnout
        elif sleep >= 6 and movement_type in ["strength", "advanced_strength", "push", "pull", "legs"]:
            memory["heavy_session_count"] = heavy_count + 1
            burnout = min(100, burnout + 8)

        # 🧘 Light session slightly reduces burnout
        elif movement_type in ["yoga", "light_workout", "stretching"]:
            burnout = max(0, burnout - 5)

        memory["burnout_risk_level"] = burnout

        # ===============================
        # 🧠 Unified XP Engine
        # ===============================

        movement_type = memory.get("movement_plan_type")
        global_intensity = memory.get("global_intensity_level", "moderate")
        hormonal_stress = memory.get("hormonal_stress_index", 0)
        mode = memory.get("life_os_mode", "wellness")

        # Base XP from intensity
        if global_intensity == "very_light":
            base_xp = 6
        elif global_intensity == "high":
            base_xp = 15
        else:
            base_xp = 10

        # Hormonal modifier
        xp_modifier = 1.0

        if hormonal_stress > 75:
            xp_modifier = 0.6
        elif hormonal_stress > 60:
            xp_modifier = 0.8
        elif hormonal_stress < 30 and mode == "performance":
            xp_modifier = 1.2

        final_xp = int(base_xp * xp_modifier)

        # 🔁 Recovery gives Mental XP instead
        if movement_type == "recovery":
            memory["mental_xp"] = memory.get("mental_xp", 0) + final_xp
        else:
            memory["xp"] = memory.get("xp", 0) + final_xp
        save_memory(memory)
        st.success("Workout logged successfully 🔥")