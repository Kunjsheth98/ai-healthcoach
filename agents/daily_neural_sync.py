from agents.health_score import calculate_health_score
from agents.predictive_burnout_engine import predictive_burnout_core
from agents.life_os_controller import update_life_os_mode

def daily_neural_sync(memory):

    # ===============================
    # 1. Automatic Stress Calculation
    # ===============================

    mood = memory.get("daily_mood", 5)
    sleep = memory.get("sleep_hours", 7)
    energy = memory.get("energy_level", 5)

    stress = (
        (10 - mood) * 0.4 +
        (7 - min(sleep, 7)) * 0.4 +
        (10 - energy) * 0.2
    )

    memory["stress_index"] = max(0, min(10, round(stress)))

    # ===============================
    # 2. Mental Score
    # ===============================

    memory["mental_score"] = max(
        0,
        min(100, 60 - (memory["stress_index"] * 5) + mood * 2)
    )

    # ===============================
    # 3. Simple Burnout Logic
    # ===============================

    if memory["stress_index"] >= 7 and sleep < 6:
        memory["burnout_risk_level"] = min(
            memory.get("burnout_risk_level", 0) + 1,
            10
        )
    else:
        memory["burnout_risk_level"] = max(
            memory.get("burnout_risk_level", 0) - 1,
            0
        )

    # ===============================
    # 4. Recalculate Health Score
    # ===============================

    calculate_health_score(memory)
    update_life_os_mode(memory)
    # ===============================
    # 5. Run Predictive Engine
    # ===============================
    predictive_burnout_core(memory)

    return memory