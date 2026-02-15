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


# =====================================================
# MAIN AI FUNCTION
# =====================================================

def ask_health_coach(memory, message, chat_history):

    # ADMIN KILL SWITCH
    if memory.get("ai_paused", False):
        return "🛑 AI is temporarily paused by administrator."
    
    # -------------------------------------------------
    # 🛑 EMERGENCY DETECTION (FIRST PRIORITY)
    # -------------------------------------------------
    if detect_emergency(message):
        return emergency_response()

    # -------------------------------------------------
    # ⚠️ RESTRICTED MEDICAL REQUEST
    # -------------------------------------------------
    if detect_restricted_request(message):
        return restricted_response()

    # -------------------------------------------------
    # 💰 DAILY BUDGET SAFETY
    # -------------------------------------------------
    if not check_budget(memory):
        return "🛑 Daily AI usage limit reached. Please try again tomorrow."

    # -------------------------------------------------
    # ⏱️ GLOBAL RATE LIMIT (ANTI-SPAM)
    # -------------------------------------------------
    allowed, reason = check_rate_limit(memory)
    if not allowed:
        return f"⛔ {reason}"

    # -------------------------------------------------
    # ⚡ FAST REQUEST LIMITER (PER MINUTE)
    # -------------------------------------------------
    if not allow_request(memory):
        return "⏳ Too many requests. Please slow down."

    # -------------------------------------------------
    # 🧠 PERSONALITY + EMOTIONAL CONTEXT
    # -------------------------------------------------

    emotion = memory.get("emotional_state", "balanced")
    personality_type = memory.get("personality_type", "adaptive")
    long_term_summary = memory.get("long_term_summary", "")

    system_prompt = f"""
You are an Indian AI Health Coach focused on wellness guidance.

User personality type: {personality_type}
User emotional state: {emotion}

Health score: {memory.get('health_score', 50)}
Health goal: {memory.get('health_goals', 'general fitness')}

Long-term user profile:
{long_term_summary}

STRICT RULES:
- Never diagnose diseases
- Never prescribe medicines
- Never change medication dosage
- Provide only lifestyle and wellness guidance
- Encourage doctor consultation for medical concerns

Keep answers short, supportive, and actionable.
"""

    # -------------------------------------------------
    # BUILD MESSAGE HISTORY
    # -------------------------------------------------

    messages = [{"role": "system", "content": system_prompt}]
    messages.extend(chat_history)
    messages.append({"role": "user", "content": message})

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
    # 📊 REGISTER USAGE + COST (AFTER SUCCESS ONLY)
    # -------------------------------------------------

    register_usage(memory)      # deployment shield tracking
    register_ai_call(memory)    # budget tracking
    register_cost(memory)       # live cost meter

    # -------------------------------------------------
    # 🛡️ FINAL OUTPUT SAFETY FILTER
    # -------------------------------------------------

    unsafe_words = [
        "diagnosis",
        "you have",
        "take this prescription"
    ]

    if any(word in reply.lower() for word in unsafe_words):
        reply += (
            "\n\n⚠️ This is general wellness guidance and not medical advice."
        )

    return reply
