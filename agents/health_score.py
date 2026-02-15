from core.memory import save_memory

def calculate_health_score(memory):

    score = 50

    if memory["sleep_hours"] >= 7:
        score += 15

    if memory["water_intake"] >= 6:
        score += 10

    if memory["exercise_done"]:
        score += 15

    score += (memory["energy_level"] - 5) * 2

    memory["health_score"] = max(0, min(100, score))

    save_memory(memory)
