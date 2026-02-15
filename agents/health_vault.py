import streamlit as st
from core.health_records import save_health_record, list_records


# --------------------------------------------------
# HEALTH RECORD VAULT UI
# --------------------------------------------------

def health_record_vault():

    st.subheader("🗂️ Health Record Vault")

    uploaded = st.file_uploader(
        "Upload prescription, report or health file",
        type=["png", "jpg", "jpeg", "pdf"]
    )

    if uploaded:

        save_health_record(uploaded)
        st.success("Record uploaded successfully ✅")

    st.divider()

    st.write("### Saved Records")

    records = list_records()

    if not records:
        st.info("No records uploaded yet.")
        return

    for r in records:
        st.write(f"📄 {r}")
