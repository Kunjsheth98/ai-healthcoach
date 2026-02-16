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
from core.budget_guard import (
    check_budget,
    register_ai_call,
    allow_request
)

from core.cost_meter import register_cost

# ---------------- INDIAN FOOD INTELLIGENCE ----------------
from agents.food_interpreter import detect_indian_food
from agents.cooking_intelligence import calculate_indian_meal, log_meal


# =====================================================
# MAIN AI FUNCTION
# =====================================================

def ask_health_coach(memory, message, chat_history):

    # -------------------------------------------------
    # 🛑 ADMIN KILL SWITCH
    # -------------------------------------------------
    if memory.get("ai_paused", False):
        return "🛑 AI is temporarily paused by administrator."

    # -------------------------------------------------
    # 🍛 INDIAN FOOD DETECTION (EARLY)
    # -------------------------------------------------
    foods, calories = detect_indian_food(message)

    if foods:
        memory.setdefault("daily_food_log", [])
        memory["daily_food_log"].append({
            "foods": foods,
            "calories": calories
        })

        food_summary = ", ".join(
            [f"{f['quantity']} {f['food']}" for f in foods]
        )

        message += (
            f"\n\nUser meal detected: {food_summary} "
            f"(~{calories} kcal). Give health feedback."
        )

    # -------------------------------------------------
    # 🛑 EMERGENCY DETECTION
    # -------------------------------------------------
    if detect_emergency(message):
        return emergency_response()

    # -------------------------------------------------
    # ⚠️ RESTRICTED MEDICAL REQUEST
    # -------------------------------------------------
    if detect_restricted_request(message):
        return restricted_response()

    # -------------------------------------------------
    # 💰 DAILY BUDGET CHECK
    # -------------------------------------------------
    if not check_budget(memory):
        return "🛑 Daily AI usage limit reached. Please try again tomorrow."

    # -------------------------------------------------
    # ⏱ GLOBAL RATE LIMIT
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
    # 🧠 PERSONALITY CONTEXT
    # -------------------------------------------------
    emotion = memory.get("emotional_state", "balanced")
    personality_type = memory.get("personality_type", "adaptive")
    long_term_summary = memory.get("long_term_summary", "")

    system_prompt = f"""
You are an Indian AI Health Coach focused on lifestyle wellness.

User personality type: {personality_type}
User emotional state: {emotion}

Health score: {memory.get('health_score', 50)}
Health goal: {memory.get('health_goals', 'general fitness')}

Long-term profile:
{long_term_summary}

STRICT RULES:
- Never diagnose diseases
- Never prescribe medicines
- Never change medication dosage
- Give lifestyle guidance only
- Encourage doctor consultation when needed

Keep answers short, supportive, and actionable.
"""

    # -------------------------------------------------
    # BUILD CHAT HISTORY
    # -------------------------------------------------
    messages = [{"role": "system", "content": system_prompt}]
    messages.extend(chat_history)
    messages.append({"role": "user", "content": message})

    # -------------------------------------------------
    # 🍛 COOKING STYLE INTELLIGENCE
    # -------------------------------------------------
    foods, calories = calculate_indian_meal(memory, message)

    if foods:
        log_meal(memory, foods, calories)

    # -------------------------------------------------
    # 🤖 OPENAI CALL
    # -------------------------------------------------
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages
        )

        reply = response.choices[0].message.content

    except Exception:
        return "⚠️ AI temporarily unavailable. Please try again shortly."

    # -------------------------------------------------
    # 📊 REGISTER USAGE
    # -------------------------------------------------
    register_usage(memory)
    register_ai_call(memory)
    register_cost(memory)

    # -------------------------------------------------
    # 🛡 OUTPUT SAFETY FILTER
    # -------------------------------------------------
    unsafe_words = [
        "diagnosis",
        "you have",
        "take this prescription"
    ]

    if any(word in reply.lower() for word in unsafe_words):
        reply += "\n\n⚠️ This is general wellness guidance and not medical advice."

    return reply
