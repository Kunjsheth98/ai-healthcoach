import os

# =====================================
# WHATSAPP SETTINGS
# =====================================

WHATSAPP_ENABLED = os.getenv("WHATSAPP_ENABLED", "False") == "True"

TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID", "")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN", "")
TWILIO_WHATSAPP_NUMBER = os.getenv(
    "TWILIO_WHATSAPP_NUMBER",
    "whatsapp:+14155238886"


)
