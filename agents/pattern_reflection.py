def generate_pattern_reflection(memory):

    sleep = memory.get("sleep_hours", 6)
    water = memory.get("water_intake", 4)
    energy = memory.get("energy_level", 5)

    insights = []

    if sleep < 6:
        insights.append("Your body is running on sleep debt.")

    if water < 5:
        insights.append("Hydration is affecting your energy rhythm.")

    if energy < 5:
        insights.append("You're likely experiencing mid-day crash cycles.")

    if not insights:
        insights.append("Your patterns show stable energy behavior.")

    memory["first_day_insights"] = insights
