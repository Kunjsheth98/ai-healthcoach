import streamlit as st
import base64
from core.config import client
from core.memory import save_memory
from agents.medicine_reminder import generate_medicine_schedule




# --------------------------------------------------
# IMAGE TO BASE64
# --------------------------------------------------

def encode_image(uploaded_file):
    return base64.b64encode(uploaded_file.read()).decode("utf-8")


# --------------------------------------------------
# AI PRESCRIPTION ANALYSIS
# --------------------------------------------------

def analyze_prescription(uploaded_file, memory):

    image_base64 = encode_image(uploaded_file)

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": """
You are a medical assistant.

Read the prescription image and extract:

- medicine name
- dosage
- frequency (morning/night/etc)

Return ONLY a clean list like:

Medicine - Dosage - Frequency
"""
            },
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "Analyze this prescription."},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{image_base64}"
                        },
                    },
                ],
            },
        ],
    )

    result = response.choices[0].message.content

    memory["medicines"].append(result)
    generate_medicine_schedule(memory)

    save_memory(memory)

    return result


# --------------------------------------------------
# UI
# --------------------------------------------------

def prescription_reader_ui(memory):

    st.subheader("💊 AI Prescription Reader")

    uploaded = st.file_uploader(
        "Upload prescription image",
        type=["png", "jpg", "jpeg"]
    )

    if uploaded:

        if st.button("Analyze Prescription"):

            with st.spinner("AI reading prescription..."):
                medicines = analyze_prescription(uploaded, memory)

            st.success("Prescription analyzed ✅")
            st.write(medicines)

    if memory.get("medicines"):
        st.divider()
        st.write("### Saved Medicines")

        for m in memory["medicines"]:
            st.info(m)
