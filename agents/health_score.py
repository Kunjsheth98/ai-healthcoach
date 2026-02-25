from core.memory import save_memory


def calculate_health_score(memory):

    sleep = memory.get("sleep_hours", 6)
    water = memory.get("water_intake", 0)
    exercise = memory.get("exercise_done", False)
    energy = memory.get("energy_level", 5)

    score = 50

    if sleep >= 7:
        score += 15

    if water >= 6:
        score += 10

    if exercise:
        score += 15

    score += (energy - 5) * 2

    memory["health_score"] = max(0, min(100, score))

    save_memory(memory)