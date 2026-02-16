# =====================================================
# AI NUTRITIONIST BRAIN
# Weekly Indian Diet Intelligence
# =====================================================

def nutritionist_brain(memory):

    memory.setdefault("daily_food_log", [])
    memory.setdefault("nutrition_insights", [])

    food_log = memory["daily_food_log"]

    if not food_log:
        return

    # -------------------------------------------------
    # LAST 7 MEALS ANALYSIS
    # -------------------------------------------------

    recent_meals = food_log[-7:]

    total_calories = sum(m.get("calories", 0) for m in recent_meals)

    # simple macro heuristics (Indian diet patterns)
    carb_score = 0
    protein_score = 0
    oil_score = 0

    for meal in recent_meals:

        foods = str(meal.get("foods", "")).lower()

        if any(f in foods for f in ["rice", "roti", "paratha"]):
            carb_score += 1

        if any(f in foods for f in ["dal", "paneer", "egg", "chicken"]):
            protein_score += 1

        if any(f in foods for f in ["fried", "butter", "ghee"]):
            oil_score += 1

    insights = []

    # -------------------------------------------------
    # PATTERN DETECTION
    # -------------------------------------------------

    if carb_score > protein_score:
        insights.append(
            "🍚 Your diet is carb-heavy this week. Add more dal, paneer or protein sources."
        )

    if protein_score < 2:
        insights.append(
            "💪 Protein intake looks low. Try adding dal, curd, paneer or eggs daily."
        )

    if oil_score >= 3:
        insights.append(
            "🧈 Oil usage seems high recently. Consider lighter cooking some days."
        )

    if total_calories > 3500:
        insights.append(
            "🔥 Weekly calorie intake is high. Add walking or lighter dinners."
        )

    if not insights:
        insights.append(
            "✅ Your eating pattern looks balanced this week. Keep going!"
        )

    memory["nutrition_insights"] = insights
