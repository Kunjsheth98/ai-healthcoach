# =====================================================
# AI HEALTH COACH (ASHA — PRODUCTION VERSION)
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

# ---------------- ASHA PERSONALITY ----------------
from agents.asha_memory import (
    update_asha_memory,
    get_asha_personality_prompt
)

# ---------------- INDIAN FOOD INTELLIGENCE ----------------
from agents.food_interpreter import detect_indian_food
from agents.cooking_intelligence import calculate_indian_meal, log_meal


# =====================================================
# MAIN AI FUNCTION
# =====================================================

def ask_health_coach(memory, message, chat_history):

    # -------------------------------------------------
    # 🧠 UPDATE ASHA MEMORY PROFILE
    # -------------------------------------------------
    update_asha_memory(memory)

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
            f"\n\nUser meal detected: {food_summary}"
            f" (~{calories} kcal). Give health feedback."
        )

    # -------------------------------------------------
    # ADMIN KILL SWITCH
    # -------------------------------------------------
    if memory.get("ai_paused", False):
        return "🛑 AI is temporarily paused by administrator."

    # -------------------------------------------------
    # 🛑 EMERGENCY CHECK
    # -------------------------------------------------
    if detect_emergency(message):
        return emergency_response()

    # -------------------------------------------------
    # ⚠️ RESTRICTED REQUEST
    # -------------------------------------------------
    if detect_restricted_request(message):
        return restricted_response()

    # -------------------------------------------------
    # 💰 BUDGET CHECK
    # -------------------------------------------------
    if not check_budget(memory):
        return "🛑 Daily AI usage limit reached. Please try again tomorrow."

    # -------------------------------------------------
    # ⏱ RATE LIMIT
    # -------------------------------------------------
    allowed, reason = check_rate_limit(memory)
    if not allowed:
        return f"⛔ {reason}"

    # -------------------------------------------------
    # ⚡ FAST REQUEST LIMIT
    # -------------------------------------------------
    if not allow_request(memory):
        return "⏳ Too many requests. Please slow down."

    # -------------------------------------------------
    # 🧠 ASHA PERSONALITY PROMPT
    # -------------------------------------------------
    asha_personality = get_asha_personality_prompt(memory)

    system_prompt = f"""
{asha_personality}

Health score: {memory.get('health_score', 50)}
Health goal: {memory.get('health_goals', 'general fitness')}

STRICT MEDICAL RULES:
- Never diagnose diseases
- Never prescribe medicines
- Never change medication dosage
- Provide lifestyle guidance only
- Encourage doctor consultation when needed
"""

    # -------------------------------------------------
    # BUILD CHAT HISTORY
    # -------------------------------------------------
    messages = [{"role": "system", "content": system_prompt}]
    messages.extend(chat_history)
    messages.append({"role": "user", "content": message})

    # -------------------------------------------------
    # ADVANCED FOOD INTELLIGENCE
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
    # REGISTER USAGE
    # -------------------------------------------------
    register_usage(memory)
    register_ai_call(memory)
    register_cost(memory)

    # -------------------------------------------------
    # FINAL SAFETY FILTER
    # -------------------------------------------------
    unsafe_words = ["diagnosis", "you have", "take this prescription"]

    if any(word in reply.lower() for word in unsafe_words):
        reply += "\n\n⚠️ This is general wellness guidance and not medical advice."

    return reply
