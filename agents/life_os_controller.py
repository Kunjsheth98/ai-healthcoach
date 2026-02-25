def update_life_os_mode(memory):

    preferred = memory.get("user_preferred_mode", "wellness")
    burnout = memory.get("burnout_risk_level", 0) / 10
    stress = memory.get("stress_index", 5)

    # Emergency override
    if burnout > 0.75:
        memory["life_os_mode"] = "wellness"
        return

    # Moderate stress override
    if burnout > 0.6 or stress >= 8:
        memory["life_os_mode"] = "resilience"
        return

    # Stable → return to user preference
    memory["life_os_mode"] = preferred