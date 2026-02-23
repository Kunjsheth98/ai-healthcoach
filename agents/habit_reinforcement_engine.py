from datetime import datetime, timedelta

def neural_habit_engine(memory):

    today = datetime.now().date()
    last_date_str = memory.get("last_checkin_date")

    if last_date_str:
        last_date = datetime.fromisoformat(last_date_str).date()

        if today == last_date:
            return  # already counted today

        if today - last_date == timedelta(days=1):
            memory["streak_days"] += 1
        else:
            memory["streak_days"] = 1
    else:
        memory["streak_days"] = 1

    memory["last_checkin_date"] = today.isoformat()

    # Behavior classification
    if memory["streak_days"] >= 21:
        memory["habit_identity"] = "Disciplined Performer"
    elif memory["streak_days"] >= 7:
        memory["habit_identity"] = "Consistency Builder"
    else:
        memory["habit_identity"] = "Habit Starter"

    consistency_score = min(100, memory.get("streak_days", 0) * 4)
    memory["consistency_score"] = consistency_score