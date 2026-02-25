import re
from datetime import datetime

STRESS_WORDS = ["overwhelmed", "stressed", "pressure", "burnout", "tired"]
ANXIETY_WORDS = ["anxious", "worried", "panic", "fear"]
NEGATIVE_SELF = ["i am useless", "i am not good enough", "i always fail"]
LOW_MOTIVATION = ["lazy", "unmotivated", "can't focus"]


def process_mental_state(memory, message):

    text = message.lower()
    # ⚡ REFLEX SPIKE DETECTOR

    memory.setdefault("reflex_alert", False)

    if any(word in text for word in ["hate", "done", "quit", "exhausted", "can't do this"]):
        memory["reflex_alert"] = True
    else:
        memory["reflex_alert"] = False
        
    memory.setdefault("mental_score", 50)
    memory.setdefault("stress_index", 5)
    memory.setdefault("anxiety_index", 5)
    memory.setdefault("motivation_level", 5)
    memory.setdefault("burnout_risk_level", 0)
    memory.setdefault("resilience_score", 50)
    memory.setdefault("mental_history", [])

    for word in STRESS_WORDS:
        if word in text:
            memory["stress_index"] = min(memory["stress_index"] + 1, 10)

    for word in ANXIETY_WORDS:
        if word in text:
            memory["anxiety_index"] = min(memory["anxiety_index"] + 1, 10)

    for phrase in NEGATIVE_SELF:
        if phrase in text:
            memory["resilience_score"] = max(memory["resilience_score"] - 2, 0)

    for word in LOW_MOTIVATION:
        if word in text:
            memory["motivation_level"] = max(memory["motivation_level"] - 1, 1)

    if memory["stress_index"] > 7 and memory["motivation_level"] < 4:
        memory["burnout_risk_level"] = min(memory["burnout_risk_level"] + 1, 10)
        calculate_burnout_velocity(memory)
        calculate_mood_volatility(memory)
        calculate_sleep_mood_correlation(memory)
        
    score = (
        100
        - (memory["stress_index"] * 5)
        - (memory["anxiety_index"] * 4)
        + (memory["resilience_score"] * 0.3)
    )

    memory["mental_score"] = max(0, min(100, round(score)))

    memory["mental_history"].append(
        {
            "timestamp": datetime.utcnow().isoformat(),
            "stress": memory["stress_index"],
            "anxiety": memory["anxiety_index"],
            "motivation": memory["motivation_level"],
            "burnout_risk_level": memory.get("burnout_risk_level", 0)
        }
    )
    # 🔥 ADVANCED MENTAL PATTERN MODEL
    history = memory.get("mental_history", [])

    if len(history) >= 5:
        recent_stress = [h.get("stress", 5) for h in history[-5:]]

        if recent_stress[-1] > recent_stress[0]:
            memory["mental_pattern"] = "stress_increasing"
        elif recent_stress[-1] < recent_stress[0]:
            memory["mental_pattern"] = "stress_improving"
        else:
            memory["mental_pattern"] = "stable"

    memory["mental_history"] = memory["mental_history"][-50:]

def post_response_learning(memory, user_message, ai_reply):

    # Simple adaptive learning example
    if "thank you" in user_message.lower():
        memory["resilience_score"] = min(memory["resilience_score"] + 1, 100)

    if "this helps" in user_message.lower():
        memory["mental_score"] = min(memory["mental_score"] + 2, 100)

def calculate_burnout_velocity(memory):
    history = memory.get("mental_history", [])

    if len(history) < 3:
        return 0

    last = history[-1].get("burnout_risk_level", 0)
    prev = history[-2].get("burnout_risk_level", 0)

    velocity = last - prev

    memory["burnout_velocity"] = velocity
    return velocity  

def calculate_mood_volatility(memory):
    log = memory.get("emotional_event_log", [])

    if len(log) < 5:
        memory["mood_volatility"] = 0
        return 0

    moods = [entry.get("mood", 5) for entry in log[-7:]]

    diffs = []
    for i in range(1, len(moods)):
        diffs.append(abs(moods[i] - moods[i - 1]))

    volatility = round(sum(diffs) / len(diffs), 2)

    memory["mood_volatility"] = volatility
    return volatility          

def calculate_sleep_mood_correlation(memory):

    log = memory.get("emotional_event_log", [])

    if len(log) < 5:
        memory["sleep_mood_correlation"] = 0
        return 0

    sleep_values = [entry.get("sleep", 0) for entry in log[-7:]]
    mood_values = [entry.get("mood", 5) for entry in log[-7:]]

    avg_sleep = sum(sleep_values) / len(sleep_values)
    avg_mood = sum(mood_values) / len(mood_values)

    numerator = sum(
        (s - avg_sleep) * (m - avg_mood)
        for s, m in zip(sleep_values, mood_values)
    )

    sleep_var = sum((s - avg_sleep) ** 2 for s in sleep_values)
    mood_var = sum((m - avg_mood) ** 2 for m in mood_values)

    denominator = (sleep_var * mood_var) ** 0.5

    correlation = numerator / denominator if denominator != 0 else 0

    memory["sleep_mood_correlation"] = round(correlation, 2)

    return correlation