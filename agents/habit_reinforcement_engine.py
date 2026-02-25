def neural_habit_engine(memory):

    memory.setdefault("streak_days", 0)

    # Behavior classification
    if memory["streak_days"] >= 21:
        memory["habit_identity"] = "Disciplined Performer"
    elif memory["streak_days"] >= 7:
        memory["habit_identity"] = "Consistency Builder"
    else:
        memory["habit_identity"] = "Habit Starter"

    consistency_score = min(100, memory["streak_days"] * 4)
    memory["consistency_score"] = consistency_score
    # 🧠 HABIT LOOP AMPLIFIER

    memory.setdefault("habit_strength", 0)

    if memory.get("streak_days", 0) >= 3:
        memory["habit_strength"] += 1

    if memory.get("streak_days", 0) >= 7:
        memory["habit_strength"] += 2

    memory["habit_strength"] = min(memory["habit_strength"], 100)

    # 🎲 VARIABLE REWARD ENGINE

    import random

    memory.setdefault("variable_reward", None)

    if memory.get("streak_days", 0) > 0:
        reward_chance = random.random()

        if reward_chance > 0.75:
            memory["variable_reward"] = "bonus_encouragement"
        else:
            memory["variable_reward"] = None