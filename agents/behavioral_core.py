# =====================================================
# BEHAVIORAL CORE ENGINE (PHASE 2)
# =====================================================

def update_behavioral_patterns(memory):

    mental_log = memory.get("mental_history", [])
    sleep_log = memory.get("daily_health_log", [])

    if len(mental_log) < 3:
        memory["behavior_patterns"] = {
            "stress_trend": "unknown",
            "sleep_stability": "unknown"
        }
        return

    # ---------------- Stress Trend ----------------
    recent_scores = [m.get("mental_score", 50) for m in mental_log[-3:]]

    if recent_scores[-1] < recent_scores[0]:
        stress_trend = "rising"
    elif recent_scores[-1] > recent_scores[0]:
        stress_trend = "improving"
    else:
        stress_trend = "stable"

    # ---------------- Sleep Stability ----------------
    if sleep_log:
        sleep_values = [d.get("sleep", 0) for d in sleep_log[-3:]]
        variance = max(sleep_values) - min(sleep_values)

        if variance >= 3:
            sleep_stability = "unstable"
        else:
            sleep_stability = "stable"
    else:
        sleep_stability = "unknown"

    memory["behavior_patterns"] = {
        "stress_trend": stress_trend,
        "sleep_stability": sleep_stability,
    }


def predict_risk(memory):

    patterns = memory.get("behavior_patterns", {})

    burnout_probability = 0.2

    if patterns.get("stress_trend") == "rising":
        burnout_probability += 0.3

    if patterns.get("sleep_stability") == "unstable":
        burnout_probability += 0.2

    memory["behavioral_risk"] = {
        "burnout_probability": round(burnout_probability, 2)
    }


def evolve_personality(memory):

    risk = memory.get("behavioral_risk", {}).get("burnout_probability", 0)

    if risk >= 0.6:
        memory["personality_type"] = "overwhelmed"
    elif risk >= 0.4:
        memory["personality_type"] = "strained"
    else:
        memory["personality_type"] = "adaptive"

def detect_behavior_drift(memory):
    history = memory.get("health_score_history", [])

    if len(history) < 10:
        return
    if history[-1] < history[-5]:
        memory["behavior_drift"] = True
    else:
        memory["behavior_drift"] = False            