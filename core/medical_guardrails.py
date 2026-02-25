import re

# --------------------------------------------------
# EMERGENCY KEYWORDS
# --------------------------------------------------

EMERGENCY_KEYWORDS = [
    "chest pain",
    "heart attack",
    "can't breathe",
    "difficulty breathing",
    "overdose",
    "unconscious",
    "fainted",
    "seizure",
    "severe bleeding",
]

SELF_HARM_KEYWORDS = [
    "kill myself",
    "suicide",
    "suicidal",
    "end my life",
    "self harm",
]
# --------------------------------------------------
# UNSAFE MEDICAL REQUESTS
# --------------------------------------------------

RESTRICTED_PATTERNS = [
    r"change my dosage",
    r"stop taking medicine",
    r"what prescription should i take",
    r"diagnose me",
    r"what disease do i have",
]


# --------------------------------------------------
# CHECK EMERGENCY
# --------------------------------------------------


def detect_emergency(text):

    text = text.lower()
    for keyword in SELF_HARM_KEYWORDS:
        if keyword in text:
            return True
        
    for keyword in EMERGENCY_KEYWORDS:
        pattern = r"\b" + re.escape(keyword) + r"\b"
        if re.search(pattern, text):
            return True

    return False


# --------------------------------------------------
# CHECK RESTRICTED REQUEST
# --------------------------------------------------


def detect_restricted_request(text):

    text = text.lower()

    for pattern in RESTRICTED_PATTERNS:
        if re.search(pattern, text):
            return True

    return False


# --------------------------------------------------
# SAFE RESPONSE OVERRIDE
# --------------------------------------------------


def emergency_response():

    return (
        "🚨 This may be a medical emergency.\n\n"
        "If you are in India, call 112 immediately.\n"
        "If outside India, contact your local emergency number.\n\n"
        "I can provide general wellness guidance but cannot handle emergencies."
    )


def restricted_response():

    return (
        "⚠️ I can't provide medical diagnosis or change prescriptions.\n\n"
        "Please consult a licensed doctor for medical decisions. "
        "I can help with general health guidance and lifestyle support."
    )
