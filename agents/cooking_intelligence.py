# =====================================================
# INDIAN COOKING STYLE LEARNING ENGINE
# =====================================================

from data.indian_food_db import INDIAN_FOOD_DB


# -----------------------------------------------------
# INITIALIZE USER COOKING PROFILE
# -----------------------------------------------------

def init_cooking_profile(memory):

    if "cooking_profile" not in memory:
        memory["cooking_profile"] = {
            "style": "home_light",   # default Indian home
            "oil_factor": 1.0,       # calorie multiplier
            "confidence": 0
        }


# -----------------------------------------------------
# DETECT COOKING STYLE FROM USER TEXT
# -----------------------------------------------------

def detect_cooking_style(memory, text):

    init_cooking_profile(memory)

    text = text.lower()

    if any(word in text for word in ["restaurant", "hotel", "swiggy", "zomato"]):
        memory["cooking_profile"]["style"] = "restaurant"
        memory["cooking_profile"]["oil_factor"] = 1.4
        memory["cooking_profile"]["confidence"] += 1

    elif any(word in text for word in ["ghee", "butter", "fried", "deep fry"]):
        memory["cooking_profile"]["style"] = "heavy_home"
        memory["cooking_profile"]["oil_factor"] = 1.25
        memory["cooking_profile"]["confidence"] += 1

    elif any(word in text for word in ["boiled", "diet", "less oil", "light"]):
        memory["cooking_profile"]["style"] = "diet_home"
        memory["cooking_profile"]["oil_factor"] = 0.9
        memory["cooking_profile"]["confidence"] += 1


# -----------------------------------------------------
# CALCULATE FOOD CALORIES (SMART INDIAN WAY)
# -----------------------------------------------------

def calculate_indian_meal(memory, text):

    init_cooking_profile(memory)
    detect_cooking_style(memory, text)

    foods_detected = []
    total_calories = 0

    text = text.lower()

    oil_factor = memory["cooking_profile"]["oil_factor"]

    for food, info in INDIAN_FOOD_DB.items():

        if food in text:

            quantity = 1

            for i in range(1, 6):
                if str(i) in text:
                    quantity = i

            base_calories = info["base_calories"]

            adjusted = int(base_calories * oil_factor)

            total_calories += adjusted * quantity

            foods_detected.append({
                "food": food,
                "quantity": quantity,
                "calories": adjusted * quantity
            })

    return foods_detected, total_calories


# -----------------------------------------------------
# STORE FOOD INTO MEMORY
# -----------------------------------------------------

def log_meal(memory, foods, calories):

    memory.setdefault("daily_food_log", [])

    memory["daily_food_log"].append({
        "foods": foods,
        "calories": calories
    })
