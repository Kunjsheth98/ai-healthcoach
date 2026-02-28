from core.memory import save_memory

def update_strategic_focus(memory):

    goal = memory.get("goal_mode", "general")
    emotional_depth = memory.get("emotional_depth_level", "low")
    burnout = memory.get("burnout_risk_level", 0)

    focus = "balanced"

    if emotional_depth == "high" or burnout >= 7:
        focus = "recovery"

    elif goal in ["fat_loss", "muscle_gain"] and burnout <= 4:
        focus = "performance"

    elif goal == "stress_reduction":
        focus = "calm_regulation"

    memory["strategic_focus"] = focus

    save_memory(memory)