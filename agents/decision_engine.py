def life_decision_engine(memory):

    burnout = memory.get("burnout_risk_level", 0)
    energy = memory.get("energy_level", 5)
    sleep = memory.get("sleep_hours", 7)

    if burnout >= 7:
        memory["strategic_focus"] = "recovery"

    elif energy >= 7 and sleep >= 7:
        memory["strategic_focus"] = "performance"

    else:
        memory["strategic_focus"] = "consistency"