def system_state_engine(memory):

    sleep = memory.get("sleep_hours", 7)
    mood = memory.get("daily_mood", 5)
    energy = memory.get("energy_level", 5)
    burnout = memory.get("burnout_risk_level", 0)
    stress = memory.get("stress_score", 0)

    # Default
    state = "balanced"

    # Overloaded condition
    if burnout >= 8:
        state = "overloaded"

    # Recovery condition
    elif sleep <= 5 and mood <= 4:
        state = "recovery"

    # Growth condition
    elif sleep >= 7 and energy >= 7 and mood >= 7:
        state = "growth"

    # Moderate stress pushes to recovery
    elif stress >= 4:
        state = "recovery"

    memory["system_state"] = state

    return state