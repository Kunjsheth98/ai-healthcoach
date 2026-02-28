def stress_engine(memory):

    lifestyle = memory.get("lifestyle", {})
    mood = memory.get("daily_mood", 5)
    sleep = memory.get("sleep_hours", 7)
    energy = memory.get("energy_level", 5)

    stress_score = 0

    # State-based stress
    if mood <= 4:
        stress_score += 2

    if sleep <= 5:
        stress_score += 2

    if energy <= 4:
        stress_score += 1

    # Personality-based stress
    if lifestyle.get("sleep_pattern") == "irregular":
        stress_score += 1

    if lifestyle.get("goal") == "reduce stress":
        stress_score += 1

    memory["stress_score"] = stress_score

    recommendations = []

    if stress_score >= 5:
        recommendations = [
            "🫁 4-7-8 breathing (5 min)",
            "📓 Write one emotional trigger today",
            "📵 No screens 1 hour before sleep",
            "🧘 10 min guided relaxation"
        ]

    elif stress_score >= 3:
        recommendations = [
            "🧘 5 min breathing reset",
            "🚶 Light 10 min walk",
            "💧 Hydration focus"
        ]

    elif stress_score >= 1:
        recommendations = [
            "🧍 Posture reset break",
            "💧 Drink water"
        ]

    memory["stress_recommendations"] = recommendations