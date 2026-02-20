import base64
from core.config import client
from core.memory import save_memory


def encode_image(uploaded_file):
    return base64.b64encode(uploaded_file.read()).decode("utf-8")


def analyze_food_image(uploaded_file, memory):

    image_base64 = encode_image(uploaded_file)

    response = client.chat.completions.create(
        model="gpt-4o-mini",
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
                        "image_url": {"url": f"data:image/jpeg;base64,{image_base64}"},
                    },
                ],
            },
        ],
    )

    result = response.choices[0].message.content or ""

    # Extract calories number roughly
    calories = 0
    for line in result.split("\n"):
        if "calories" in line.lower():
            digits = "".join([c for c in line if c.isdigit()])
            if digits:
                calories = int(digits)

    memory.setdefault("daily_food_log", [])
    memory["daily_food_log"].append({"image_analysis": result, "calories": calories})

    save_memory(memory)

    return result
