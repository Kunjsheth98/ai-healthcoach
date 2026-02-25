def generate_future_projection(memory):

    sleep = memory.get("sleep_hours", 6)
    exercise = memory.get("exercise_done", False)
    burnout = memory.get("burnout_risk_level", 0)
    streak = memory.get("streak_days", 0)
    energy = memory.get("energy_level", 5)
    momentum = memory.get("burnout_momentum", 0)

    if burnout >= 7:
        projection = (
            "If this stress pattern continues, high burnout risk may develop within 2–3 months."
        )

    elif momentum > 1:
        projection = (
            "Stress acceleration detected. Without intervention, energy stability may decline."
        )

    elif sleep < 6 and not exercise:
        projection = (
            "If nothing changes, chronic fatigue risk increases within 6 months."
        )

    elif streak >= 7 and energy >= 7:
        projection = (
            "If you maintain this consistency, your resilience and metabolic efficiency will significantly improve."
        )

    else:
        projection = (
            "With small daily improvements, your health trajectory is trending positively."
        )

    memory["future_projection"] = projection