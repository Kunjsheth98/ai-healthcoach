# =====================================================
# IDENTITY EVOLUTION ENGINE
# Gradually upgrades psychological identity
# =====================================================

def evolve_identity(memory):

    if not memory.get("imprint_identity"):
        return

    stability = memory.get("identity_stability", 0)
    streak = memory.get("streak_days", 0)
    engagement = memory.get("engagement_score", 0)

    growth_score = streak + (engagement // 5)

    # Increase stability slowly
    stability += growth_score * 0.05
    stability = min(stability, 100)

    memory["identity_stability"] = round(stability, 2)

    # Upgrade identity tiers
    if stability >= 70:
        memory["imprint_identity"] = "The Self-Mastered"
    elif stability >= 40:
        memory["imprint_identity"] = "The Emerging Force"