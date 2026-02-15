import streamlit as st
from core.memory import save_memory

# -----------------------------------
# DAILY AI BUDGET LIMIT
# -----------------------------------

MAX_DAILY_AI_CALLS = 120   # safe testing limit


def init_budget(memory):

    if "budget" not in memory:
        memory["budget"] = {
            "ai_calls_today": 0
        }


def check_budget(memory):

    init_budget(memory)

    if memory["budget"]["ai_calls_today"] >= MAX_DAILY_AI_CALLS:
        return False

    return True


def register_ai_call(memory):

    init_budget(memory)

    memory["budget"]["ai_calls_today"] += 1
    save_memory(memory)
