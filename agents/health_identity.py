def classify_health_identity(memory):

    sleep = memory.get("sleep_hours", 6)
    energy = memory.get("energy_level", 5)
    exercise = memory.get("exercise_done", False)

    memory.setdefault("identity_stability", 0)
    memory.setdefault("health_identity", None)

    previous = memory["health_identity"]

    # ---- Identity Classification ----
    if sleep < 6 and energy < 5:
        identity = "Overworked Achiever"
    elif not exercise and energy < 6:
        identity = "Inconsistent Starter"
    elif exercise and sleep >= 7:
        identity = "High-Potential Performer"
    else:
        identity = "Silent Stress Carrier"

    # ---- Stability Mechanism ----
    if identity == previous:
        memory["identity_stability"] = 0
        return

    memory["identity_stability"] += 1

    # Change only if repeated pattern
    if memory["identity_stability"] >= 2:
        memory["health_identity"] = identity
        memory["identity_stability"] = 0