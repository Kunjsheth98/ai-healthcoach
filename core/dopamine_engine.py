# =====================================================
# DOPAMINE MICRO REWARD ENGINE
# Subtle reinforcement boosts
# =====================================================

def dopamine_trigger(memory):

    attachment = memory.get("attachment_score", 0)
    stability = memory.get("identity_stability", 0)

    if attachment > 20 and stability > 10:
        return "You’re evolving faster than you realize."

    if attachment > 40:
        return "Your consistency is becoming rare."

    if attachment > 70:
        return "This is no longer effort. This is identity."

    return None