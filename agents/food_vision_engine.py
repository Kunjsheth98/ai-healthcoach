import base64
from core.config import client
from core.memory import save_memory
from core.ai_wrapper import call_ai


def encode_image(uploaded_file):
    return base64.b64encode(uploaded_file.read()).decode("utf-8")


def analyze_food_image(uploaded_file, memory):

    image_base64 = encode_image(uploaded_file)
    # Basic size protection (5MB limit)
    if uploaded_file.size > 5 * 1024 * 1024:
        return "⚠️ Image too large. Please upload under 5MB."
    
    messages=[
        {
            "role": "system",
            "content": """
    You are a nutrition AI.

    Analyze the meal image.

    Return in this format:

    Food: <items>
    Estimated Calories: <number>
    Health Feedback: <short advice>
    """,
                },
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "Analyze this food image."},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{image_base64}"
                            },
                        },
            ],
        },
    ]
    

    result = call_ai(memory, messages)
    if not result:
        result = "⚠️ Image analysis unavailable. Please describe your meal manually."

    # Extract calories number roughly
    import re

    calories = 0
    match = re.search(r"(\d{2,4})", result)
    if match:
        calories = int(match.group(1))

    # Store vision result temporarily
    memory["last_vision_result"] = {
        "analysis": result,
        "calories": calories
    }

    return result
