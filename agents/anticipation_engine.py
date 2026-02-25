def anticipatory_suggestion(memory):

    energy = memory.get("energy_level", 5)
    burnout = memory.get("burnout_risk_level", 0)
    streak = memory.get("streak_days", 0)
    momentum = memory.get("burnout_momentum", 0)

    # Rising burnout trend
    if burnout >= 6 or momentum > 1:
        return "Reduce tomorrow’s workload and prioritize recovery."

    # Low energy pattern
    elif energy <= 3:
        return "Hydrate early and add a short mid-day reset to avoid crash."

    # High consistency → growth window
    elif streak >= 10 and burnout < 4:
        return "You are stable — gradually increase intensity this week."

    return None