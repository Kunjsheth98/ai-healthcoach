import time
from core.memory import save_memory

# -----------------------------------
# CONFIG
# -----------------------------------

MAX_DAILY_AI_CALLS = 120      # request limit
DAILY_COST_LIMIT = 3.0        # USD safety budget
MAX_REQUESTS_PER_MINUTE = 10  # spam protection


# -----------------------------------
# INIT
# -----------------------------------

def init_budget(memory):

    if "budget" not in memory:
        memory["budget"] = {
            "ai_calls_today": 0,
            "daily_cost": 0.0,
            "request_times": []
        }


# -----------------------------------
# CALL LIMIT CHECK
# -----------------------------------

def check_budget(memory):

    init_budget(memory)

    if memory["budget"]["ai_calls_today"] >= MAX_DAILY_AI_CALLS:
        return False

    if memory["budget"]["daily_cost"] >= DAILY_COST_LIMIT:
        return False

    return True


# -----------------------------------
# REGISTER AI CALL
# -----------------------------------

def register_ai_call(memory, estimated_cost=0.002):

    init_budget(memory)

    memory["budget"]["ai_calls_today"] += 1
    memory["budget"]["daily_cost"] += estimated_cost

    save_memory(memory)


# -----------------------------------
# RATE LIMITER
# -----------------------------------

def allow_request(memory):

    init_budget(memory)

    now = time.time()

    memory["budget"]["request_times"] = [
        t for t in memory["budget"]["request_times"]
        if now - t < 60
    ]

    if len(memory["budget"]["request_times"]) >= MAX_REQUESTS_PER_MINUTE:
        return False

    memory["budget"]["request_times"].append(now)
    save_memory(memory)

    return True


# -----------------------------------
# GET COST
# -----------------------------------

def get_today_cost(memory):
    init_budget(memory)
    return memory["budget"]["daily_cost"]
