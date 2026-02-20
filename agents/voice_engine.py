import streamlit as st
from gtts import gTTS
import tempfile
import os


def speak_text(text, language="en"):

    tts = gTTS(text=text, lang=language)

    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
        tts.save(fp.name)
        audio_file = open(fp.name, "rb")
        audio_bytes = audio_file.read()

    st.audio(audio_bytes, format="audio/mp3")
