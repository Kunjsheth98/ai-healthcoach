from agents.health_score import calculate_health_score
from agents.predictive_burnout_engine import predictive_burnout_core


def daily_neural_sync(memory):

    # ===============================
    # 1. Sync Stress From Lifestyle
    # ===============================
    lifestyle = memory.get("lifestyle", {})
    memory["stress_index"] = lifestyle.get("stress_level", memory.get("stress_index", 5))

    # ===============================
    # 2. Sync Mood → Mental Score
    # ===============================
    mood = memory.get("daily_mood", 5)
    sleep = memory.get("sleep_hours", 7)
    energy = memory.get("energy_level", 5)

    # Simple mental formula
    memory["mental_score"] = max(
        0,
        min(100, 50 + (mood * 3) + (sleep * 2) - (memory["stress_index"] * 3))
    )

    # ===============================
    # 3. Burnout Basic Update
    # ===============================
    if memory["stress_index"] >= 8 and sleep < 6:
        memory["burnout_risk_level"] += 1

    memory["burnout_risk_level"] = min(memory["burnout_risk_level"], 10)

    # ===============================
    # 4. Recalculate Health Score
    # ===============================
    calculate_health_score(memory)

    # ===============================
    # 5. Run Predictive Engine
    # ===============================
    predictive_burnout_core(memory)

    return memory