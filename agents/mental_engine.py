import re
from datetime import datetime

STRESS_WORDS = ["overwhelmed", "stressed", "pressure", "burnout", "tired"]
ANXIETY_WORDS = ["anxious", "worried", "panic", "fear"]
NEGATIVE_SELF = ["i am useless", "i am not good enough", "i always fail"]
LOW_MOTIVATION = ["lazy", "unmotivated", "can't focus"]


def process_mental_state(memory, message):

    text = message.lower()

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
        
    memory["mental_score"] = max(
        0,
        100
        - (memory["stress_index"] * 5)
        - (memory["anxiety_index"] * 4)
        + (memory["resilience_score"] * 0.3),
    )

    memory["mental_history"].append(
        {
            "timestamp": datetime.utcnow().isoformat(),
            "stress": memory["stress_index"],
            "anxiety": memory["anxiety_index"],
            "motivation": memory["motivation_level"],
            "burnout_risk_level": memory.get("burnout_risk_level", 0)
        }
    )

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

    correlation = 0
    for s, m in zip(sleep_values, mood_values):
        correlation += (s - avg_sleep) * (m - avg_mood)

    memory["sleep_mood_correlation"] = round(correlation, 2)
    return correlation