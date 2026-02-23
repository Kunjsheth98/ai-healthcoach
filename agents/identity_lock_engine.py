

def identity_lock_system(memory):

    streak = memory.get("streak_days", 0)
    burnout = memory.get("burnout_risk_level", 0)
    engagement = memory.get("engagement_score", 0)

    if burnout >= 8:
        identity = "Recovery Mode"

    elif streak >= 30:
        identity = "Unstoppable Discipline"

    elif streak >= 14:
        identity = "High Consistency Performer"

    elif engagement >= 20:
        identity = "Growth Focused"

    else:
        identity = "Building Momentum"

    memory.setdefault("identity_lock", {})
    memory["identity_lock"]["current_identity"] = identity

    return identity
