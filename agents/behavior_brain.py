# =====================================================
# BEHAVIOR INTELLIGENCE BRAIN
# Habit Relapse + Motivation + Engagement Predictor
# =====================================================


def behavior_brain(memory):

    memory.setdefault("behavior_alerts", [])
    memory.setdefault("daily_health_log", [])

    logs = memory["daily_health_log"]

    if len(logs) < 5:
        return

    recent = logs[-7:]

    avg_energy = sum(d.get("energy", 5) for d in recent) / len(recent)
    energy_trend = recent[-1].get("energy",5) - recent[0].get("energy",5)
    sleep_trend = recent[-1].get("sleep",6) - recent[0].get("sleep",6)
    exercise_days = sum(1 for d in recent if d.get("exercise"))
    avg_sleep = sum(d.get("sleep", 6) for d in recent) / len(recent)

    alerts = []

    # -------------------------------------------------
    # RELAPSE RISK
    # -------------------------------------------------

    if exercise_days <= 1:
        alerts.append("⚠️ Habit relapse risk detected. Activity consistency dropping.")

    # -------------------------------------------------
    # MOTIVATION DROP
    # -------------------------------------------------

    if avg_energy < 5:
        alerts.append(
            "🧠 Motivation levels appear low. Try lighter goals for a few days."
        )

    # -------------------------------------------------
    # BURNOUT SIGNAL
    # -------------------------------------------------

    if avg_sleep < 5:
        alerts.append("🔥 Burnout signal detected. Recovery and sleep needed.")

    # Early decline detection
    if energy_trend < -2:
        alerts.append("📉 Energy trend declining over the week.")

    if sleep_trend < -2:
        alerts.append("😴 Sleep quality worsening over recent days.")
    # -------------------------------------------------
    # POSITIVE MOMENTUM
    # -------------------------------------------------

    if exercise_days >= 4 and avg_energy >= 7:
        alerts.append("🚀 Strong habit momentum detected. Keep this streak going!")
    engagement = memory.get("engagement_score", 0)

    if engagement < 3 and len(recent) >= 7:
        alerts.append("⚠️ Engagement dropping. Reconnect with your core goal.")
        
    memory["behavior_alerts"] = alerts
