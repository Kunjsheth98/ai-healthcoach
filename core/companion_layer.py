# =====================================================
# COMPANION LAYER
# Simplifies UX while keeping engine intact
# =====================================================

from datetime import datetime


def get_time_greeting():
    hour = datetime.now().hour

    if hour < 12:
        return "Good morning"
    elif hour < 18:
        return "Good afternoon"
    else:
        return "Good evening"


def determine_primary_focus(memory):

    # If user already selected intent
    if "primary_intent" in memory:
        return memory["primary_intent"]

    # Automatic fallback logic
    if memory.get("burnout_risk_level", 0) >= 6:
        return "stress"

    if memory.get("sleep_hours", 7) < 6:
        return "sleep"

    if not memory.get("exercise_done", False):
        return "movement"

    return "general"


def companion_message(memory):

    greeting = get_time_greeting()
    focus = determine_primary_focus(memory)

    if focus == "sleep":
        message = "Let’s stabilize your sleep step by step."
    elif focus == "stress":
        message = "Today we reduce pressure, not increase it."
    elif focus == "movement":
        message = "Let’s add light movement today."
    else:
        message = "We’ll improve one small thing today."

    return f"{greeting}. {message}"