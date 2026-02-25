def neural_consistency_engine(memory):

    goal = memory.get("lifestyle", {}).get("goal", "")
    calories = sum(entry.get("calories", 0) for entry in memory.get("daily_food_log", []))
    exercise = memory.get("exercise_done", False)

    inconsistency = False

    profile = memory.get("profile", {})
    weight = profile.get("weight_kg", 70)

    # Rough maintenance estimate
    maintenance = weight * 30

    if goal == "Fat loss":
        if calories > maintenance and not exercise:
            inconsistency = True

    memory["consistency_flag"] = inconsistency
    memory["consistency_score_flag"] = not inconsistency