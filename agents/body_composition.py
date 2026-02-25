def calculate_body_fat(memory):

    profile = memory.get("profile", {})
    height_cm = profile.get("height_cm")
    weight_kg = profile.get("weight_kg")
    gender = profile.get("gender")

    if not height_cm or not weight_kg:
        return

    height_m = height_cm / 100

    if height_m <= 0:
        return

    bmi = weight_kg / (height_m ** 2)

    # Basic estimate formula
    if gender == "Male":
        body_fat = (1.20 * bmi) + (0.23 * profile.get("age", 25)) - 16.2
    else:
        body_fat = (1.20 * bmi) + (0.23 * profile.get("age", 25)) - 5.4

    # Clamp realistic human range
    body_fat = max(5, min(body_fat, 50))

    memory["body_fat_percentage"] = round(body_fat, 1)
