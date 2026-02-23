def neural_consistency_engine(memory):

    goal = memory.get("lifestyle", {}).get("goal", "")
    calories = sum(entry.get("calories", 0) for entry in memory.get("daily_food_log", []))
    exercise = memory.get("exercise_done", False)

    inconsistency = False

    if goal == "weight_loss":
        if calories > 2500 and not exercise:
            inconsistency = True

    memory["consistency_flag"] = inconsistency