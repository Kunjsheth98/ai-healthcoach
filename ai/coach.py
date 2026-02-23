# =====================================================
# AI HEALTH COACH (SAFE + PRODUCTION VERSION)
# =====================================================

from core.config import client

# ---------------- SAFETY GUARDRAILS ----------------
from core.medical_guardrails import (
    detect_emergency,
    detect_restricted_request,
    emergency_response,
    restricted_response,
)

# ---------------- RATE LIMIT SHIELD ----------------
from core.deployment_shield import check_rate_limit, register_usage

# ---------------- BUDGET + COST CONTROL ----------------
from core.budget_guard import check_budget, register_ai_call, allow_request

from core.cost_meter import register_cost

# ---------------- INDIAN FOOD INTELLIGENCE ----------------
from agents.food_interpreter import detect_indian_food
from agents.cooking_intelligence import calculate_indian_meal, log_meal

from agents.mental_engine import process_mental_state, post_response_learning
from core.subscription import has_premium_access

from agents.behavioral_core import (
    update_behavioral_patterns,
    predict_risk,
    evolve_personality,
)
from agents.predictive_burnout_engine import predictive_burnout_core
# =====================================================
# MAIN AI FUNCTION
# =====================================================


def ask_health_coach(memory, message, chat_history, uploaded_image=None):

    # -------------------------------------------------
    # 🍛 INDIAN FOOD DETECTION
    # -------------------------------------------------
    foods, calories = detect_indian_food(message)

    if foods:
        memory.setdefault("daily_food_log", [])
        memory["daily_food_log"].append({"foods": foods, "calories": calories})

        food_summary = ", ".join([f"{f['quantity']} {f['food']}" for f in foods])

        message += (
            f"\n\nUser meal detected: {food_summary} "
            f"(~{calories} kcal). Give health feedback."
        )

    # -------------------------------------------------
    # ADMIN KILL SWITCH
    # -------------------------------------------------
    if memory.get("ai_paused", False):
        return "🛑 AI is temporarily paused by administrator."

    # -------------------------------------------------
    # 🛑 EMERGENCY DETECTION
    # -------------------------------------------------
    if detect_emergency(message):
        return emergency_response()

    # -------------------------------------------------
    # ⚠️ RESTRICTED REQUEST
    # -------------------------------------------------
    if detect_restricted_request(message):
        return restricted_response()

    # -------------------------------------------------
    # 💰 DAILY BUDGET CHECK
    # -------------------------------------------------
    if not check_budget(memory):
        return "🛑 Daily AI usage limit reached."

    # -------------------------------------------------
    # ⏱️ GLOBAL RATE LIMIT
    # -------------------------------------------------
    allowed, reason = check_rate_limit(memory)
    if not allowed:
        return f"⛔ {reason}"

    # -------------------------------------------------
    # ⚡ FAST REQUEST LIMITER
    # -------------------------------------------------
    if not allow_request(memory):
        return "⏳ Too many requests. Please slow down."

    # -------------------------------------------------
    # 🧠 PREMIUM MENTAL ENGINE
    # -------------------------------------------------
    if has_premium_access("mental_engine"):
        process_mental_state(memory, message)

    # -------------------------------------------------
    # 🧠 PROFILE + WEIGHT TREND CONTEXT
    # -------------------------------------------------

    emotion = memory.get("emotional_state", "balanced")
    long_term_summary = memory.get("long_term_summary", "")

    profile = memory.get("profile", {})
    lifestyle = memory.get("lifestyle", {})
    weight_history = memory.get("weight_history", [])

    weight_trend = "No recent weight data."
    profile_context = f"""
    User Name: {profile.get('name')}
    Age: {profile.get('age')}
    Gender: {profile.get('gender')}
    Height: {profile.get('height_cm')} cm
    Weight: {profile.get('weight_kg')} kg
    Diseases: {profile.get('diseases')}
    Primary Goal: {lifestyle.get('goal')}
    Activity Level: {lifestyle.get('activity_type')}
    Sleep Pattern: {lifestyle.get('sleep_pattern')}
    """
    if len(weight_history) >= 2:
        first = weight_history[0]["weight"]
        last = weight_history[-1]["weight"]
        diff = last - first

        if diff > 0:
            weight_trend = f"User gained {diff} kg recently."
        elif diff < 0:
            weight_trend = f"User lost {abs(diff)} kg recently."
        else:
            weight_trend = "User weight stable."
    profile_context += f"\nWeight Trend:\n{weight_trend}"      

        
    future_prediction = ""

    if len(weight_history) >= 2:
        first = weight_history[0]["weight"]
        last = weight_history[-1]["weight"]
        diff = last - first

        if diff != 0:
            monthly_projection = diff * 4
            future_prediction = f"If trend continues, body may change by {monthly_projection} kg in 30 days."

    calorie_adjustment = ""

    if "body_fat_percentage" in memory:
        bf = memory["body_fat_percentage"]

        if bf > 25:
            calorie_adjustment = "User should follow moderate calorie deficit."
        elif bf < 15:
            calorie_adjustment = "User should avoid deficit and focus on strength."
        else:
            calorie_adjustment = "Maintain balanced calories."

    mental_context = f"""
    Stress Level: {lifestyle.get('stress_level')}
    Emotional State: {emotion}
    """
    brain = memory.get("brain_state", {})
    brain_mode = brain.get("mode", "wellness")
    intervention = brain.get("intervention", "normal")

    tone = "balanced"

    if intervention == "force_recovery":
        tone = "calm, slow, grounding and recovery-focused"

    elif intervention == "intensity_reduction":
        tone = "supportive, structured and balanced"

    else:
        if brain_mode == "performance":
            tone = "focused, goal-driven and high performance"
        elif brain_mode == "discipline":
            tone = "firm, structured and accountability-focused"
        elif brain_mode == "resilience":
            tone = "supportive and emotionally grounding"
        else:
            tone = "calm, balanced and wellness-oriented"   

    suppression = memory.get("suppression_state", "none")

    if suppression == "high":
        tone = "calm, grounding and pressure-free"
    elif suppression == "moderate":
        tone = "supportive and balanced"       
# ---------------- PHASE 2 BEHAVIOR UPDATE ----------------
    update_behavioral_patterns(memory)
    predict_risk(memory)
    evolve_personality(memory)
    predictive_burnout_core(memory)
    from agents.personality_engine import evolve_personality_from_habits
    evolve_personality_from_habits(memory)

# ---------------- CENTRAL COACH AUTHORITY ----------------
    burnout = memory.get("burnout_risk_level", 0)

    if burnout >= 7:
        memory["brain_state"] = {
            "mode": "recovery_lock",
            "intervention": "force_recovery"
        }
    elif burnout >= 4:
        memory["brain_state"] = {
            "mode": memory.get("life_os_mode", "wellness"),
            "intervention": "intensity_reduction"
        }
    else:
        memory["brain_state"] = {
            "mode": memory.get("life_os_mode", "wellness"),
            "intervention": "normal"
        }

    personality = memory.get("personality_type", "Balanced Guide")
    volatility = memory.get("mood_volatility", 0)
    correlation = memory.get("sleep_mood_correlation", 0)

    intelligence_layer = f"""
    Mood Volatility: {volatility}
    Sleep-Mood Correlation: {correlation}
    Active Personality Mode: {personality}
    """
    # =========================================
    # FIRST 3 INTERACTION INTELLIGENCE BOOST
    # =========================================

    interaction_count = memory.get("interaction_count", 0)
    memory["interaction_count"] = interaction_count + 1

    boost_instruction = ""

    if interaction_count < 3:
        boost_instruction = """
You are in onboarding intelligence mode.

This is one of the first 3 interactions.

Do these things:

1. Infer the user's main goal.
2. Infer their energy pattern.
3. Infer stress pattern if visible.
4. Infer personality tone (disciplined, emotional, analytical, etc.)

Then say:

"Here’s what I understand about you so far..."

Summarize briefly.

Then ask ONE sharp, intelligent reflective question.

Make the user feel deeply seen.
"""
    else:
        boost_instruction = "" 
    system_prompt = f"""
You are Asha — an Indian AI Health Coach.
Your tone should be {tone}.
{boost_instruction}

Identity Lock:
{memory.get("identity_lock", {}).get("current_identity")}
Reinforce this identity in encouragement.

Behavior Intelligence:
Behavior Intelligence:
{intelligence_layer}
User personality type: {personality}
User emotional state: {emotion}

Health score: {memory.get('health_score', 50)}

User Profile:
{profile_context}

Long-term profile summary:
{long_term_summary}

Calorie Strategy:
{calorie_adjustment}

30-Day Projection:
{future_prediction}

Mental Health Context:
{mental_context}
Mood Trend: {memory.get('mood_trend', 'stable')}
Behavior Patterns:
{memory.get("behavior_patterns")}

Risk Forecast:
{memory.get("risk_forecast")}
Identity Lock:
{memory.get("identity_lock", {}).get("current_identity")}
Reinforce this identity subtly in tone and encouragement.

STRICT RULES:
- Never diagnose diseases
- Never prescribe medicines
- Never change dosage
- Only lifestyle & wellness coaching
"""

    # -------------------------------------------------
    # BUILD MESSAGE HISTORY
    # -------------------------------------------------

    messages = [{"role": "system", "content": system_prompt}]
    messages.extend(chat_history)
    messages.append({"role": "user", "content": message})
    memory["last_message_depth"] = min(10, len(message.split()) // 10)

    if memory.get("burnout_momentum", 0) > 1:
        reflection_note = "\nUser stress seems to be increasing over time."
    else:
        reflection_note = ""

    message += reflection_note
    memory["last_message_depth"] = min(10, len(message.split()) // 10)
    # -------------------------------------------------
    # 🍛 COOKING INTELLIGENCE ENGINE
    # -------------------------------------------------

    foods, calories = calculate_indian_meal(memory, message)

    if foods:
        log_meal(memory, foods, calories)

    # -------------------------------------------------
    # 🤖 OPENAI CALL
    # -------------------------------------------------

    try:
        response = client.chat.completions.create(
    model="gpt-4o-mini", messages=messages  # type: ignore
    )
        reply = response.choices[0].message.content or ""
        engagement = memory.get("engagement_score", 0)

        if engagement % 3 == 0 and engagement != 0:
            reply += "\n\n🔥 You're building strong momentum. Keep showing up."
    except Exception:
        reply = (
            "⚠️ Asha is currently in offline mode.\n\n"
            "AI responses are paused because API billing is not active.\n"
            "Your app UI and health tracking are still working normally."
        )

    # -------------------------------------------------
    # 🧠 POST RESPONSE LEARNING (OUTSIDE TRY)
    # -------------------------------------------------
    if has_premium_access("mental_engine"):
        post_response_learning(memory, message, reply)

    # -------------------------------------------------
    # 📊 REGISTER USAGE + COST
    # -------------------------------------------------

    register_usage(memory)
    register_ai_call(memory)
    register_cost(memory)

    # -------------------------------------------------
    # 🛡️ FINAL SAFETY FILTER
    # -------------------------------------------------

    unsafe_words = ["diagnosis", "you have", "take this prescription"]

    if any(word in reply.lower() for word in unsafe_words):
        reply += "\n\n⚠️ This is general wellness guidance, not medical advice."

    return reply
