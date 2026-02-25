import streamlit as st
# =====================================================
# AI NUTRITIONIST BRAIN
# Weekly Indian Diet Intelligence
# =====================================================
from core.config import client
from core.memory import save_memory
from core.ai_wrapper import call_ai

def nutritionist_brain(memory):

    mode = memory.get("life_os_mode", "wellness")

     # ================= CENTRAL BRAIN OVERRIDE =================
    brain_mode = memory.get("brain_state", {}).get("mode")

    if brain_mode == "recovery_lock":
        st.subheader("🥗 AI Nutritionist")
        st.warning("⚠ Recovery Nutrition Mode")
        st.success("""
    Today focus on:
    - Hydration (3L water)
    - Magnesium rich foods (banana, nuts)
    - Avoid aggressive calorie deficit
    - Balanced carbs for stress recovery
    """)
        return
    
    if brain_mode == "load_reduction":
        st.subheader("🥗 AI Nutritionist")
        st.info("⚠ Moderate Nutrition Mode")
        st.success("""
Maintain balanced calories.
Avoid heavy fasting.
Increase protein and hydration.
""")
        return
    
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
        insights.append("✅ Your eating pattern looks balanced this week. Keep going!")


    brain = memory.get("brain_state", {})
    brain_mode = brain.get("mode", "wellness")
    suppression = memory.get("suppression_state", "none")

    if suppression == "high":
        insights.append("Focus on light digestion and hydration this week.")

    system_prompt = f"""
    You are Asha — an Indian AI Nutritionist.

    Brain Mode: {brain_mode}
    Detected Weekly Insights: {insights}
    Identity: {memory.get("identity_lock", {}).get("current_identity")}
    Reinforce identity subtly.

    Refine this into:
    - What to improve
    - What to maintain
    - One simple action

    Keep short.
    Do not diagnose.
    """

    if len(insights) <= 1:
        memory["nutrition_insights"] = insights
    else:
        
        messages=[{"role": "system", "content": system_prompt}],
        refined = call_ai(memory, messages)
        if refined:
            memory["nutrition_insights"] = [refined]

    save_memory(memory)