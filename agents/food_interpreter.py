# =====================================================
# INDIAN FOOD INTERPRETER AGENT
# =====================================================

import re
from data.indian_food_db import INDIAN_FOOD_DB


def detect_indian_food(text):

    text = text.lower()

    foods_found = []

    for food, info in INDIAN_FOOD_DB.items():

        if re.search(r"\b" + re.escape(food) + r"\b", text):

            quantity = 1

            match = re.search(r"(\d+)\s*" + re.escape(food), text)
            if match:
                quantity = int(match.group(1))

            foods_found.append(
                {"food": food, "quantity": quantity}
            )

    return foods_found, 0
