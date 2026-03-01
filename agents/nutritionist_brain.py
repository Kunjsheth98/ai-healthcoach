import streamlit as st
# =====================================================
# AI NUTRITIONIST BRAIN
# Weekly Indian Diet Intelligence
# =====================================================
from core.config import client
from core.memory import save_memory
from core.ai_wrapper import call_ai

def nutritionist_brain(memory):

    global_intensity = memory.get("global_intensity_level", "moderate")
    calorie_target = memory.get("daily_calorie_target")


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
        st.subheader("🥗 AI Nutritionist")
        st.info("Log your meals to receive adaptive weekly nutrition intelligence.")
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

    # ===============================
    # Hormonal Phase Nutrition Layer
    # ===============================

    phase = memory.get("current_cycle_phase")

    if phase == "menstrual":
        insights.append("🩸 During menstrual phase, prioritize iron-rich foods (spinach, lentils) and hydration.")

    elif phase == "follicular":
        insights.append("🌱 Follicular phase supports lighter meals and protein building.")

    elif phase == "ovulatory":
        insights.append("🔥 Ovulatory phase benefits from balanced carbs and strength-support nutrition.")

    elif phase == "luteal":
        insights.append("🌙 Luteal phase may increase cravings. Focus on stable blood sugar and magnesium-rich foods.")

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

    if global_intensity == "very_light":
        insights.append("⚡ Focus on recovery nutrition: hydration, magnesium, simple digestion.")

    elif global_intensity == "high":
        insights.append("🔥 Increase protein and structured meals to support higher load.")   

    if calorie_target is not None:
        insights.append(f"🎯 Today's adaptive calorie target: {calorie_target} kcal.")     

    if memory.get("weekly_calorie_adjustment"):
        insights.append("📊 Calorie target auto-adjusted based on last 7 days intake trend.")    

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
    Imprint Identity: {memory.get('imprint_identity','emerging')}
    Emotional Archetype: {memory.get('emotional_archetype','neutral')}

    Identity Maturity Level: {memory.get("identity_maturity","forming")}

    Strategic Focus: {memory.get("strategic_focus","balanced")}

    If Strategic Focus = recovery:
    Avoid calorie deficit.

    If Strategic Focus = performance:
    Optimize protein and macro structure.

    If Strategic Focus = calm_regulation:
    Prioritize digestion-friendly foods.

    If Identity Maturity = forming:
    Avoid aggressive calorie restriction.
    Focus on simple habit upgrades.

    If Identity Maturity = emerging:
    Encourage structured meal timing and protein focus.

    If Identity Maturity = solid:
    Emphasize macro awareness and consistency.

    If Identity Maturity = integrated:
    Align nutrition tightly with performance and body composition goals.

    If Archetype = overloaded:
    Avoid aggressive calorie restriction.

    If Archetype = self_critical:
    Avoid guilt framing.

    If Archetype = achiever:
    Emphasize performance nutrition.
    Global Intensity: {global_intensity}

    If Global Intensity = very_light:
    Focus on recovery nutrition only.
    Avoid calorie deficit.

    If Global Intensity = high:
    Increase protein recommendation.
    Support recovery meals.

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
        
        messages=[{"role": "system", "content": system_prompt}]
        refined = call_ai(memory, messages)
        if refined:
            memory["nutrition_insights"] = [refined]

    save_memory(memory)