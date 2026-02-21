from statistics import mean

def predictive_burnout_core(memory):

    mental_history = memory.get("mental_history", [])
    daily_log = memory.get("daily_health_log", [])

    if len(mental_history) < 4:
        return

    # ===============================
    # 1️⃣ Stress Acceleration
    # ===============================
    stress_values = [m.get("stress_index", 5) for m in mental_history[-6:]]
    stress_acceleration = (stress_values[-1] - stress_values[-3]) if len(stress_values) >= 3 else 0

    # ===============================
    # 2️⃣ Sleep Recovery Deficit
    # ===============================
    sleep_values = [d.get("sleep", 7) for d in daily_log[-6:]]
    avg_sleep = mean(sleep_values) if sleep_values else 7
    sleep_deficit = max(0, 7 - avg_sleep)

    sleep_trend = sleep_values[-1] - sleep_values[-3] if len(sleep_values) >= 3 else 0
    worsening_sleep = 1 if sleep_trend < 0 else 0

    # ===============================
    # 3️⃣ Emotional Instability
    # ===============================
    mood_values = [m.get("motivation_level", 5) for m in mental_history[-6:]]
    mood_volatility = max(mood_values) - min(mood_values) if mood_values else 0
    instability_amplifier = mood_volatility * 1.5

    memory["mood_volatility"] = mood_volatility

    # ===============================
    # 4️⃣ Burnout Momentum
    # ===============================
    burnout_values = [m.get("burnout_risk_level", 0) for m in mental_history[-4:]]
    burnout_momentum = burnout_values[-1] - burnout_values[0]
    memory["burnout_velocity"] = burnout_momentum

    # ===============================
    # 5️⃣ Engagement Stability
    # ===============================
    engagement = memory.get("engagement_score", 0)
    engagement_penalty = 2 if engagement < 2 else 0

    # ===============================
    # 6️⃣ Recovery Capacity Score
    # ===============================
    resilience = memory.get("resilience_score", 50)
    recovery_buffer = resilience / 25  # higher resilience reduces risk

    # ===============================
    # 7️⃣ Neural Composite Risk
    # ===============================
    neural_score = (
        stress_acceleration * 2
        + sleep_deficit * 2
        + worsening_sleep * 2
        + instability_amplifier
        + burnout_momentum * 2
        + engagement_penalty
        - recovery_buffer
    )

    probability = min(max(neural_score / 25, 0), 1)

    # ===============================
    # Dynamic Forecast Window
    # ===============================
    if probability > 0.75:
        forecast_days = 2
    elif probability > 0.6:
        forecast_days = 3
    elif probability > 0.4:
        forecast_days = 5
    else:
        forecast_days = 7

    # ===============================
    # Trigger Classification
    # ===============================
    triggers = {
        "Stress Escalation": stress_acceleration,
        "Sleep Deficit Pattern": sleep_deficit,
        "Emotional Instability": mood_volatility,
        "Burnout Momentum": burnout_momentum,
    }

    primary_trigger = max(triggers.items(), key=lambda x: x[1])[0]

    # ===============================
    # Intervention Tier
    # ===============================
    if probability > 0.75:
        intervention = "Immediate Recovery Protocol"
    elif probability > 0.6:
        intervention = "Moderate Load Reduction"
    elif probability > 0.4:
        intervention = "Preventive Recovery Adjustment"
    else:
        intervention = "Stable"

    memory["risk_forecast"] = {
        "burnout_probability": probability,
        "forecast_days": forecast_days,
        "primary_trigger": primary_trigger,
        "intervention_level": intervention,
    }

    # ===============================
    # Central Brain Mode Override
    # ===============================
    if probability > 0.75:
        brain_mode = "recovery_lock"
    elif probability > 0.6:
        brain_mode = "load_reduction"
    elif probability > 0.4:
        brain_mode = "preventive_care"
    else:
        brain_mode = "performance_mode"

    memory["brain_state"] = {
        "mode": brain_mode,
        "burnout_probability": probability
    }