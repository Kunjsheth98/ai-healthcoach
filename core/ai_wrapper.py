from core.config import client
from core.budget_guard import register_ai_call
from core.deployment_shield import register_usage
from core.memory import save_memory

def call_ai(memory, messages, model="gpt-4o-mini"):
    # 🧠 META RESOURCE ALLOCATION

    if memory.get("burnout_risk_level", 0) >= 8:
        model = "gpt-4o-mini"

    elif memory.get("evolution_stage", 1) >= 3:
        model = "gpt-4o"

    elif memory.get("risk_confidence_score", 50) > 80:
        model = "gpt-4o-mini"
    try:
        response = client.chat.completions.create(
            model=model,
            messages=messages
        )

        reply = response.choices[0].message.content or ""

        register_usage(memory)
        register_ai_call(memory)

        return reply

    except Exception:
        return None