# =====================================================
# INDIAN FOOD INTERPRETER AGENT
# =====================================================

import re
from data.indian_food_db import INDIAN_FOOD_DB


def detect_indian_food(text):

    text = text.lower()

    foods_found = []
    total_calories = 0

    for food, info in INDIAN_FOOD_DB.items():

        if food in text:

            # detect quantity (default = 1)
            quantity = 1

            match = re.search(r"(\d+)\s*" + food, text)
            if match:
                quantity = int(match.group(1))

            calories = info["calories"] * quantity

            foods_found.append(
                {"food": food, "quantity": quantity, "calories": calories}
            )

            total_calories += calories

    return foods_found, total_calories
