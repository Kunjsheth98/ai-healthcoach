from core.memory import save_memory

def update_emotional_resonance(memory, message):

    memory.setdefault("emotional_resonance_history", [])

    vulnerability_keywords = [
        "tired", "exhausted", "overwhelmed",
        "stressed", "anxious", "lost",
        "confused", "burnt", "hopeless"
    ]

    vulnerability_score = 0

    msg = message.lower()

    for word in vulnerability_keywords:
        if word in msg:
            vulnerability_score += 1

    memory["emotional_resonance_history"].append(vulnerability_score)

    # keep last 20 interactions
    memory["emotional_resonance_history"] = memory["emotional_resonance_history"][-20:]

    avg = sum(memory["emotional_resonance_history"]) / len(memory["emotional_resonance_history"])

    memory["emotional_resonance_score"] = round(avg, 2)

    if avg >= 2:
        memory["emotional_depth_level"] = "high"
    elif avg >= 1:
        memory["emotional_depth_level"] = "medium"
    else:
        memory["emotional_depth_level"] = "low"

    save_memory(memory)