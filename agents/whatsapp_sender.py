from twilio.rest import Client
from core.whatsapp_config import (
    WHATSAPP_ENABLED,
    TWILIO_ACCOUNT_SID,
    TWILIO_AUTH_TOKEN,
    TWILIO_WHATSAPP_NUMBER,
)

# --------------------------------------------------
# SEND WHATSAPP MESSAGE
# --------------------------------------------------


def send_whatsapp_message(user_number, message):

    if not WHATSAPP_ENABLED:
        return

    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

    client.messages.create(
        body=message, from_=TWILIO_WHATSAPP_NUMBER, to=f"whatsapp:{user_number}"
    )
