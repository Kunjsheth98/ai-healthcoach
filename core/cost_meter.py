from core.memory import save_memory

# -----------------------------------
# COST SETTINGS (APPROX GPT-4o-mini)
# -----------------------------------

# approx cost per request (safe estimate)
COST_PER_REQUEST_USD = 0.002   # ~$0.002 per response
USD_TO_INR = 83


# -----------------------------------
# INITIALIZE COST TRACKING
# -----------------------------------

def init_cost(memory):

    if "cost_tracking" not in memory:
        memory["cost_tracking"] = {
            "requests_today": 0,
            "usd_spent": 0.0
        }


# -----------------------------------
# REGISTER COST
# -----------------------------------

def register_cost(memory):

    init_cost(memory)

    memory["cost_tracking"]["requests_today"] += 1
    memory["cost_tracking"]["usd_spent"] += COST_PER_REQUEST_USD

    save_memory(memory)


# -----------------------------------
# GET COST SUMMARY
# -----------------------------------

def get_cost_summary(memory):

    init_cost(memory)

    usd = memory["cost_tracking"]["usd_spent"]
    inr = usd * USD_TO_INR

    return (
        memory["cost_tracking"]["requests_today"],
        round(usd, 3),
        round(inr, 2)
    )
