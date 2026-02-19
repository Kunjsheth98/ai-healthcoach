def classify_health_identity(memory):

    sleep = memory.get("sleep_hours", 6)
    energy = memory.get("energy_level", 5)
    exercise = memory.get("exercise_done", False)

    if sleep < 6 and energy < 5:
        identity = "Overworked Achiever"
    elif not exercise and energy < 6:
        identity = "Inconsistent Starter"
    elif exercise and sleep >= 7:
        identity = "High-Potential Performer"
    else:
        identity = "Silent Stress Carrier"

    memory["health_identity"] = identity
