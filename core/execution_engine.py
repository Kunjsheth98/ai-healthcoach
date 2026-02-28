from core.memory import save_memory

def update_execution_score(memory):

    memory.setdefault("execution_history", [])

    score = 0

    # Workout completion
    if memory.get("exercise_done"):
        score += 1

    # Food logging consistency
    if len(memory.get("daily_food_log", [])) > 0:
        score += 1

    # Planner engagement
    if memory.get("structured_plan"):
        score += 1

    memory["execution_history"].append(score)

    memory["execution_history"] = memory["execution_history"][-14:]

    avg = sum(memory["execution_history"]) / len(memory["execution_history"])

    memory["execution_score"] = round(avg * 33.3, 2)  # scale to 0–100

    save_memory(memory)