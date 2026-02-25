def classify_user(memory):
    streak = memory.get("streak_days", 0)
    engagement = memory.get("engagement_score", 0)

    if streak >= 14:
        segment = "High Performer"
    elif engagement >= 20:
        segment = "Growth Oriented"
    else:
        segment = "Beginner"

    memory["user_segment"] = segment            