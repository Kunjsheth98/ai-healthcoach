from agents.stress_engine import stress_engine
from agents.system_state_engine import system_state_engine
from agents.hormonal_intelligence import hormonal_intelligence_core
from agents.metabolic_predictor import metabolic_predictor
from agents.behavior_brain import behavior_brain
from agents.health_identity import classify_health_identity
from agents.health_score import calculate_health_score
from datetime import date

def life_os_orchestrator(memory):

    today = str(date.today())

    # make sure key exists
    last_run = memory.get("last_orchestrator_run")

    # run heavy engines only once per day
    if last_run != today:

        try:
            stress_engine(memory)
            system_state_engine(memory)

            hormonal_intelligence_core(memory)

            metabolic_predictor(memory)
            behavior_brain(memory)

            classify_health_identity(memory)
            calculate_health_score(memory)

            memory["last_orchestrator_run"] = today

        except Exception as e:
            memory["orchestrator_error"] = str(e)