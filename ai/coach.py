from core.config import client

from core.medical_guardrails import (
    detect_emergency,
    detect_restricted_request,
    emergency_response,
    restricted_response,
)

from core.deployment_shield import check_rate_limit, register_usage
from core.budget_guard import check_budget, register_ai_call, allow_request
from core.cost_meter import register_cost

from agents.food_interpreter import detect_indian_food
from agents.cooking_intelligence import calculate_indian_meal, log_meal
from agents.asha_memory import update_asha_memory


def ask_health_coach(memory, message, chat_history):

    # ================= FOOD DETECTION =================
    foods, calories = detect_indian_food(message)

    if foods:
        memory.setdefault("daily_food_log", [])
        memory["daily_food_log"].append(
            {"foods": foods, "calories": calories}
        )

        summary = ", ".join(
            [f"{f['quantity']} {f['food']}" for f in foods]
        )

        message += f"\nUser meal detected: {summary} (~{calories} kcal). Give feedback."

    # ================= SAFETY =================
    if memory.get("ai_paused"):
        return "🛑 AI temporarily paused."

    if detect_emergency(message):
        return emergency_response()

    if detect_restricted_request(message):
        return restricted_response()

    # ================= LIMITS =================
    if not check_budget(memory):
        return "🛑 Daily limit reached."

    allowed, reason = check_rate_limit(memory)
    if not allowed:
        return reason

    if not allow_request(memory):
        return "⏳ Slow down."

    # ================= PERSONALITY =================
    emotion = memory.get("emotional_state", "balanced")
    personality = memory.get("personality_type", "adaptive")

    system_prompt=f"""
You are Asha, an Indian AI Health Coach.

Emotion: {emotion}
Personality: {personality}

Rules:
- No diagnosis
- No medicines
- Lifestyle guidance only
- Keep responses short and supportive.
"""

    messages=[{"role":"system","content":system_prompt}]
    messages.extend(chat_history)
    messages.append({"role":"user","content":message})

    foods, calories = calculate_indian_meal(memory, message)
    if foods:
        log_meal(memory, foods, calories)

    # ================= OPENAI =================
    try:
        response=client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages
        )
        reply=response.choices[0].message.content
    except Exception:
        return "⚠️ AI temporarily unavailable."

    register_usage(memory)
    register_ai_call(memory)
    register_cost(memory)

    update_asha_memory(memory, message, reply)

    return reply
