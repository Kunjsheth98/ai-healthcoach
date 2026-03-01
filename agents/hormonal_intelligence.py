from datetime import datetime, timedelta


# =====================================================
# HORMONAL CYCLE ENGINE
# =====================================================

def update_cycle_data(memory, cycle_start_date, cycle_length=28):
    """
    Stores cycle configuration.
    """
    memory["cycle_tracking"] = {
        "cycle_start_date": cycle_start_date,
        "cycle_length": cycle_length
    }


def calculate_cycle_phase(memory):

    cycle_data = memory.get("cycle_tracking")
    if not cycle_data:
        return None, None, None

    start_date_str = cycle_data.get("cycle_start_date")
    cycle_length = cycle_data.get("cycle_length", 28)

    if not start_date_str:
        return None, None, None

    start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()
    today = datetime.now().date()

    days_since_start = (today - start_date).days % cycle_length

    # Phase Mapping
    if days_since_start <= 4:
        phase = "menstrual"
    elif days_since_start <= 12:
        phase = "follicular"
    elif days_since_start <= 16:
        phase = "ovulatory"
    else:
        phase = "luteal"

    # Estimate next period
    days_until_next_cycle = cycle_length - days_since_start
    next_period_date = today + timedelta(days=days_until_next_cycle)

    return phase, days_since_start, next_period_date


def hormonal_intelligence_core(memory):

    result = calculate_cycle_phase(memory)

    if not result:
        return memory

    phase, days_since_start, next_period_date = result

    memory["current_cycle_phase"] = phase
    memory["cycle_day"] = days_since_start
    memory["next_period_estimate"] = str(next_period_date)

    # Adjust system behavior
    if phase == "menstrual":
        memory["global_intensity_level"] = "very_light"
        memory["brain_state"]["intervention"] = "force_recovery"

    elif phase == "follicular":
        memory["global_intensity_level"] = "moderate"

    elif phase == "ovulatory":
        memory["global_intensity_level"] = "high"

    elif phase == "luteal":
        memory["global_intensity_level"] = "moderate"
        memory["brain_state"]["intervention"] = "intensity_reduction"

    return memory