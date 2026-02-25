import streamlit as st
from gtts import gTTS
import tempfile
import os


def speak_text(text, language="en"):

    try:
        tts = gTTS(text=text, lang=language)

        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
            temp_path = fp.name
            tts.save(temp_path)

        with open(temp_path, "rb") as audio_file:
            audio_bytes = audio_file.read()

        st.audio(audio_bytes, format="audio/mp3")

    except Exception:
        st.warning("⚠️ Voice service unavailable.")

    finally:
        if 'temp_path' in locals() and os.path.exists(temp_path):
            os.remove(temp_path)
