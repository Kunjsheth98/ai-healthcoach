def stress_engine(memory):

    lifestyle = memory.get("lifestyle", {})
    goal = lifestyle.get("goal", "")
    sleep_pattern = lifestyle.get("sleep_pattern", "")
    discipline = lifestyle.get("discipline_score", 5)

    stress_score = 0

    if goal == "reduce stress":
        stress_score += 2

    if sleep_pattern == "irregular":
        stress_score += 2

    if discipline <= 3:
        stress_score += 1

    if memory.get("daily_mood", 5) <= 4:
        stress_score += 2

    memory["stress_score"] = stress_score

    recommendations = []

    if stress_score >= 4:
        recommendations.append("5-minute guided breathing")
        recommendations.append("Short mobility break")
        recommendations.append("Evening digital detox")

    elif stress_score >= 2:
        recommendations.append("Light stretching")
        recommendations.append("Hydration focus")

    memory["stress_recommendations"] = recommendations