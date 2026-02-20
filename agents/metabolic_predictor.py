# =====================================================
# METABOLIC PREDICTOR ENGINE
# Preventive Health Intelligence
# =====================================================


def metabolic_predictor(memory):

    memory.setdefault("metabolic_alerts", [])
    memory.setdefault("daily_health_log", [])

    health_log = memory["daily_health_log"]

    # Need enough history
    if len(health_log) < 5:
        return

    recent = health_log[-7:]

    avg_sleep = sum(d.get("sleep", 0) for d in recent) / len(recent)
    avg_energy = sum(d.get("energy", 5) for d in recent) / len(recent)
    avg_water = sum(d.get("water", 0) for d in recent) / len(recent)
    exercise_days = sum(1 for d in recent if d.get("exercise"))

    alerts = []

    # -----------------------------------
    # FATIGUE RISK
    # -----------------------------------

    if avg_sleep < 6 and avg_energy < 5:
        alerts.append("😴 Fatigue risk detected. Low sleep and energy trend observed.")

    # -----------------------------------
    # DEHYDRATION TREND
    # -----------------------------------

    if avg_water < 4:
        alerts.append("💧 Hydration levels low this week. Increase water intake.")

    # -----------------------------------
    # ACTIVITY DECLINE
    # -----------------------------------

    if exercise_days <= 1:
        alerts.append("🏃 Activity drop detected. Body metabolism may slow.")

    # -----------------------------------
    # RECOVERY STATE (GOOD SIGNAL)
    # -----------------------------------

    if avg_sleep >= 7 and avg_energy >= 7:
        alerts.append("✅ Recovery trend strong. Your body is responding well.")

    memory["metabolic_alerts"] = alerts
