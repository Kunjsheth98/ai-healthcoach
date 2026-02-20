# =====================================================
# 🧠 ASHA MEMORY PERSONALITY ENGINE
# =====================================================


def update_asha_memory(memory):

    memory.setdefault("asha_profile", {})

    profile = memory["asha_profile"]

    # -----------------------------------
    # Habit consistency learning
    # -----------------------------------

    streak = memory.get("streak_days", 0)
    energy = memory.get("energy_level", 5)
    sleep = memory.get("sleep_hours", 6)

    if streak >= 7:
        profile["user_type"] = "disciplined"
    elif energy <= 4:
        profile["user_type"] = "low_energy"
    elif sleep < 6:
        profile["user_type"] = "burnout_risk"
    else:
        profile["user_type"] = "balanced"

    # -----------------------------------
    # Coaching tone selection
    # -----------------------------------

    tone_map = {
        "disciplined": "challenging",
        "low_energy": "supportive",
        "burnout_risk": "calming",
        "balanced": "motivational",
    }

    profile["coach_tone"] = tone_map.get(profile["user_type"], "motivational")


def get_asha_personality_prompt(memory):

    profile = memory.get("asha_profile", {})
    tone = profile.get("coach_tone", "motivational")
    user_type = profile.get("user_type", "balanced")

    personality_prompt = f"""
You are ASHA, a caring Indian AI Health Coach.

User behavioral type: {user_type}
Your coaching tone: {tone}

Behavior rules:
- supportive → gentle encouragement
- calming → reduce pressure, focus recovery
- motivational → energizing guidance
- challenging → push performance carefully

Speak like a real human coach.
Be emotionally intelligent.
Keep responses short and actionable.
"""

    return personality_prompt
