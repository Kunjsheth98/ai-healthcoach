import time
from datetime import datetime
from core.memory import save_memory


# =====================================================
# CONFIGURATION
# =====================================================

MAX_DAILY_AI_CALLS = 120       # max AI calls per day
DAILY_COST_LIMIT = 3.0         # default daily budget (USD)
MAX_REQUESTS_PER_MINUTE = 10   # anti-spam protection


# =====================================================
# INITIALIZE MEMORY STRUCTURE
# =====================================================

def init_budget(memory):

    if "budget" not in memory:
        memory["budget"] = {
            "ai_calls_today": 0,
            "daily_cost": 0.0,
            "request_times": []
        }

    if "ai_paused" not in memory:
        memory["ai_paused"] = False

    if "last_reset_date" not in memory:
        memory["last_reset_date"] = datetime.utcnow().date().isoformat()


# =====================================================
# DAILY AUTO RESET SYSTEM
# =====================================================

def daily_reset(memory):

    init_budget(memory)

    today = datetime.utcnow().date().isoformat()

    # If new day → reset everything
    if memory["last_reset_date"] != today:

        memory["last_reset_date"] = today

        memory["budget"]["ai_calls_today"] = 0
        memory["budget"]["daily_cost"] = 0.0
        memory["budget"]["request_times"] = []

        # Auto resume AI next day
        memory["ai_paused"] = False

        save_memory(memory)


# =====================================================
# BUDGET + LIMIT CHECK
# =====================================================

def check_budget(memory):

    daily_reset(memory)
    init_budget(memory)

    # Admin custom limit (fallback default)
    admin_limit = memory.get("admin_budget_limit", DAILY_COST_LIMIT)

    # Auto shutdown when cost reached
    if memory["budget"]["daily_cost"] >= admin_limit:
        memory["ai_paused"] = True
        save_memory(memory)
        return False

    # Call limit safety
    if memory["budget"]["ai_calls_today"] >= MAX_DAILY_AI_CALLS:
        return False

    # Manual admin pause
    if memory.get("ai_paused", False):
        return False

    return True


# =====================================================
# REGISTER AI CALL + COST
# =====================================================

def register_ai_call(memory, estimated_cost=0.002):

    init_budget(memory)

    memory["budget"]["ai_calls_today"] += 1
    memory["budget"]["daily_cost"] += estimated_cost

    save_memory(memory)


# =====================================================
# RATE LIMITER (ANTI SPAM)
# =====================================================

def allow_request(memory):

    init_budget(memory)

    now = time.time()

    # keep only last 60 seconds
    memory["budget"]["request_times"] = [
        t for t in memory["budget"]["request_times"]
        if now - t < 60
    ]

    if len(memory["budget"]["request_times"]) >= MAX_REQUESTS_PER_MINUTE:
        return False

    memory["budget"]["request_times"].append(now)
    save_memory(memory)

    return True


# =====================================================
# COST DISPLAY HELPER
# =====================================================

def get_today_cost(memory):

    init_budget(memory)
    return memory["budget"]["daily_cost"]
