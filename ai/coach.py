# =====================================================
# AI HEALTH COACH (SAFE + PRODUCTION VERSION)
# =====================================================

from core.config import client
from core.ai_wrapper import call_ai

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

# ---------------- INDIAN FOOD INTELLIGENCE ----------------
from agents.food_interpreter import detect_indian_food
from agents.cooking_intelligence import calculate_indian_meal, log_meal

from agents.mental_engine import process_mental_state, post_response_learning
from core.subscription import has_premium_access
from core.emotional_imprint_engine import emotional_imprint_engine
from core.dopamine_engine import dopamine_trigger

from agents.behavioral_core import (
    update_behavioral_patterns,
    predict_risk,
    evolve_personality,
)
from agents.predictive_burnout_engine import predictive_burnout_core
from agents.personality_engine import evolve_personality_from_habits
from agents.asha_memory import update_asha_memory, get_asha_personality_prompt
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
        first = weight_history[-2]["weight"]
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

    # ⚡ REFLEX HARD BRAKE

    if memory.get("reflex_alert"):
        suppression = "high"
        tone = "calm, grounding and stabilizing"

    # 🧘 META SILENCE INTELLIGENCE
    if memory.get("meta_strategy") == "prioritize_sleep":
        suppression = "high"

    if suppression == "high":
        tone = "calm, grounding and pressure-free"
    elif suppression == "moderate":
        tone = "supportive and balanced"       
# ---------------- PHASE 2 BEHAVIOR UPDATE ----------------
    update_behavioral_patterns(memory)
    predict_risk(memory)
    evolve_personality(memory)
    predictive_burnout_core(memory)
    evolve_personality_from_habits(memory)
    update_asha_memory(memory)
    asha_prompt = get_asha_personality_prompt(memory)

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
{asha_prompt}
{boost_instruction}

Behavior Intelligence:
{intelligence_layer}
User personality type: {personality}
Perception Layer:
Based on historical behavior, adapt subtle tone shifts.
Reference past tendencies when possible.
If patterns exist, mention them confidently.
User emotional state: {emotion}
Mental Pattern Trend: {memory.get("mental_pattern", "stable")}

Health score: {memory.get('health_score', 50)}

Goal Mode: {memory.get("goal_mode", "general")}
Evolution Stage: {memory.get("evolution_stage",1)}
Coach Style: {memory.get("active_prompt_style", memory.get("adaptive_coach_style","supportive"))}
Difficulty Modifier: {memory.get("difficulty_modifier",1.0)}

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

Historical Signals:
{memory.get("pattern_memory")[-3:] if memory.get("pattern_memory") else "No strong pattern yet"}

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

After giving advice, explain briefly why this suggestion was made based on user patterns.
"""

    # -------------------------------------------------
    # BUILD MESSAGE HISTORY
    # -------------------------------------------------
    if memory.get("burnout_momentum", 0) > 1:
        reflection_note = "\nUser stress seems to be increasing over time."
    else:
        reflection_note = ""

    message += reflection_note
    messages = [{"role": "system", "content": system_prompt}]
    messages.extend(chat_history)
    messages.append({"role": "user", "content": message})
    # ================= PERCEPTION MEMORY =================

    memory.setdefault("pattern_memory", [])

    if len(memory["pattern_memory"]) < 20:
        memory["pattern_memory"].append({
            "energy": memory.get("energy_level", 5),
            "stress": memory.get("stress_index", 5),
            "mood": memory.get("daily_mood", 5)
        })
    memory["last_message_depth"] = min(10, len(message.split()) // 10)

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

    reply = call_ai(memory, messages)

    # 🔥 Dopamine Reinforcement Layer
    dopamine = dopamine_trigger(memory)
    if dopamine:
        reply = (reply or "") + "\n\n" + dopamine

    # 🔥 Emotional Imprint Layer (First Interaction Only)
    imprint = emotional_imprint_engine(memory, message)
    if imprint:
        reply = imprint + "\n\n" + (reply or "")

    # 🚨 RELAPSE RESPONSE BOOST
    if memory.get("relapse_risk"):
        reply = (reply or "") + "\n\n⚠️ I sense your momentum slipping slightly. Let's protect your streak today."

    # ⚡ REFLEX MICRO REINFORCEMENT
    if memory.get("reflex_alert"):
        reply = "Pause. Take a slow breath with me for 10 seconds.\n\n" + (reply or "")
    if not reply:
        reply = ("⚠️ Asha is currently in offline mode.\n\n"
            "AI responses are paused because API billing is not active.\n"
            "Your app UI and health tracking are still working normally.")
    engagement = memory.get("engagement_score", 0)    

    if engagement % 3 == 0 and engagement != 0:
        reply += "\n\n🔥 You're building strong momentum. Keep showing up."

    # 🔥 Identity Reinforcement
    if memory.get("imprint_identity") and engagement > 3:
        reply += f"\n\nYou're stepping into your identity: {memory.get('imprint_identity')}."    
        
        

    # -------------------------------------------------
    # 🧠 POST RESPONSE LEARNING (OUTSIDE TRY)
    # -------------------------------------------------
    if has_premium_access("mental_engine"):
        post_response_learning(memory, message, reply)

    # 🧠 RESPONSE EFFECTIVENESS TRACKING

    memory.setdefault("response_scores", [])

    engagement = memory.get("engagement_score", 0)

    score = 1

    if "thank" in message.lower():
        score += 1

    if memory.get("mental_pattern") == "stress_improving":
        score += 1

    memory["response_scores"].append(score)

    memory["response_scores"] = memory["response_scores"][-50:]    

    # -------------------------------------------------
    # 🛡️ FINAL SAFETY FILTER
    # -------------------------------------------------

    unsafe_words = ["diagnosis", "you have", "take this prescription"]

    if any(word in reply.lower() for word in unsafe_words):
        reply += "\n\n⚠️ This is general wellness guidance, not medical advice."
    # AI CONFIDENCE SCORE
    confidence = 100 - (memory.get("burnout_risk_level", 0) *5)
    if memory.get("mental_pattern") == "stress_increasing":
        confidence -= 10
    if memory.get("behavior_drift"):
        confidence -= 5    
    memory["last_ai_confidence"] = max(40, confidence)
    return reply
