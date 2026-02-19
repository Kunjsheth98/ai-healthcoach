def generate_future_projection(memory):

    sleep = memory.get("sleep_hours", 6)
    exercise = memory.get("exercise_done", False)

    if sleep < 6 and not exercise:
        projection = (
            "If nothing changes, chronic fatigue risk increases within 6 months."
        )
    else:
        projection = (
            "If you maintain this pattern, energy resilience will improve steadily."
        )

    memory["future_projection"] = projection
