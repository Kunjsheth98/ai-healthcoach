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
    # 🍛 INDIAN FOOD DETECTION
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
    # 🧠 PERSONALITY CONTEXT (ASHA MEMORY)
    # -------------------------------------------------
    emotion = memory.get("emotional_state", "balanced")
    personality_type = memory.get("personality_type", "adaptive")
    long_term_summary = memory.get("long_term_summary", "")

    system_prompt = f"""
You are Asha — an Indian AI Health Coach.

User personality type: {personality_type}
User emotional state: {emotion}

Health score: {memory.get('health_score', 50)}
Heath goal: {memory.get('health_goals','general fitness')}

Long-term profile:
{long_term_summary}

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
            model="gpt-4o-mini",
            messages=messages
        )
        reply = response.choices[0].message.content

    except Exception:
        # OFFLINE SAFE MODE
        reply = (
            "⚠️ Asha is currently in offline mode.\n\n"
            "AI responses are paused because API billing is not active.\n"
            "Your app UI and health tracking are still working normally."
        )

    # -------------------------------------------------
    # 📊 REGISTER USAGE + COST (ALWAYS RUN)
    # -------------------------------------------------

    register_usage(memory)
    register_ai_call(memory)
    register_cost(memory)

    # -------------------------------------------------
    # 🛡️ FINAL SAFETY FILTER
    # -------------------------------------------------

    unsafe_words = [
        "diagnosis",
        "you have",
        "take this prescription"
    ]

    if any(word in reply.lower() for word in unsafe_words):
        reply += "\n\n⚠️ This is general wellness guidance, not medical advice."

    return reply
