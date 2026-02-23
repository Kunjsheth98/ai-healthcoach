from statistics import mean

def predictive_burnout_core(memory):

    # ==============================
    # 1️⃣ SMOOTHED STRESS
    # ==============================

    mental_history = memory.get("mental_history", [])
    recent = mental_history[-3:]

    if recent:
        stress = mean([m.get("stress_index", 5) for m in recent])
    else:
        stress = memory.get("stress_index", 5)

    memory["smoothed_stress"] = round(stress, 2)

    # ==============================
    # 2️⃣ CORE FACTORS
    # ==============================

    sleep = memory.get("sleep_hours", 7)
    energy = memory.get("energy_level", 5)
    mood = memory.get("daily_mood", 5)
    workload = memory.get("lifestyle", {}).get("discipline_score", 5)

    sleep_factor = max(0, (7 - sleep) * 1.2)
    stress_factor = stress * 1.5
    energy_factor = max(0, (5 - energy) * 1.3)
    mood_factor = max(0, (5 - mood) * 1.2)
    workload_factor = workload * 0.8

    risk_score = (
        sleep_factor +
        stress_factor +
        energy_factor +
        mood_factor +
        workload_factor
    )

    burnout_level = min(int(risk_score / 3), 10)
    memory["burnout_risk_level"] = burnout_level

    # ==============================
    # 3️⃣ BURNOUT MOMENTUM (4-day slope)
    # ==============================

    if len(mental_history) >= 4:
        recent = mental_history[-4:]
        stress_values = [m.get("stress_index", 5) for m in recent]

        momentum = (
            (stress_values[-1] - stress_values[-2]) +
            (stress_values[-2] - stress_values[-3])
        ) / 2
    else:
        momentum = 0

    memory["burnout_momentum"] = momentum

    # ==============================
    # 4️⃣ PROBABILITY MODEL
    # ==============================

    probability = min(
        1,
        (burnout_level * 0.1) + (momentum * 0.05)
    )

    memory["risk_forecast"] = {
        "burnout_probability": round(probability, 2),
        "primary_trigger": "Stress acceleration" if momentum > 1 else "Stable",
        "severity": (
            "Critical" if burnout_level >= 8
            else "Elevated" if burnout_level >= 5
            else "Normal"
        )
    }

    return burnout_level