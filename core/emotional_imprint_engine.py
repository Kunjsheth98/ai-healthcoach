# =====================================================
# EMOTIONAL IMPRINT ENGINE
# First Interaction Psychological Hook
# =====================================================

def detect_emotional_archetype(message):

    msg = message.lower()

    if any(word in msg for word in ["tired", "exhausted", "burnt", "overwhelmed"]):
        return "overloaded"

    if any(word in msg for word in ["lazy", "procrastinating", "not disciplined"]):
        return "self_critical"

    if any(word in msg for word in ["goal", "achieve", "optimize", "improve"]):
        return "achiever"

    if any(word in msg for word in ["lost", "confused", "stuck"]):
        return "drifting"

    return "neutral"


def generate_imprint_response(archetype):

    responses = {
        "overloaded": (
            "I can sense you’re carrying more than your nervous system can process right now.\n\n"
            "You're not lazy. You're overloaded.\n\n"
            "Let’s reduce pressure before we increase performance."
        ),

        "self_critical": (
            "You’re not lacking discipline.\n\n"
            "You’re stuck in a self-judgment loop.\n\n"
            "We don’t fix this with pressure. We fix this with identity realignment."
        ),

        "achiever": (
            "You’re wired for growth.\n\n"
            "But your system needs sustainability, not just intensity.\n\n"
            "We optimize intelligently, not aggressively."
        ),

        "drifting": (
            "You don’t lack motivation.\n\n"
            "You lack direction clarity.\n\n"
            "Let’s rebuild focus from first principles."
        ),

        "neutral": (
            "Let’s start by understanding your internal rhythm.\n\n"
            "Small calibrations create long-term dominance."
        )
    }

    return responses.get(archetype, responses["neutral"])


def emotional_imprint_engine(memory, user_message):

    # Only trigger on first interaction
    if memory.get("emotional_imprint_done"):
        return None

    archetype = detect_emotional_archetype(user_message)
    imprint = generate_imprint_response(archetype)

    memory["emotional_archetype"] = archetype
    memory["emotional_imprint_done"] = True
    # Assign Identity Label
    identity_map = {
        "overloaded": "The Silent Fighter",
        "self_critical": "The Hidden Potential",
        "achiever": "The Relentless Builder",
        "drifting": "The Rebuilder",
        "neutral": "The Calibrator"
    }

    identity = identity_map.get(archetype, "The Calibrator")

    memory["imprint_identity"] = identity
    memory["identity_stability"] = 0  # evolves later
    memory["attachment_depth"] = "forming"

    return imprint

def generate_personal_insight(memory, message):
    mood = memory.get("daily_mood", 5)
    energy = memory.get("energy_level", 5)
    goal = memory.get("lifestyle", {}).get("goal", "")
    phase = memory.get("current_cycle_phase")

    insight = "Here’s what I’m noticing about you so far:\n\n"

    if mood <= 4:
        insight += "- You might be carrying emotional fatigue.\n"
    elif mood >= 8:
        insight += "- You currently have strong emotional momentum.\n"

    if energy <= 4:
        insight += "- Your energy reserves seem low.\n"
    elif energy >= 8:
        insight += "- Your system has high output capacity right now.\n"

    if goal:
        insight += f"- Your main goal is {goal.lower()}.\n"

    if phase:
        insight += f"- You’re currently in {phase} phase, which affects performance and mood.\n"

    insight += "\nLet’s build intelligently from here."

    return insight