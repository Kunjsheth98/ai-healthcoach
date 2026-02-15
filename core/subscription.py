from core.app_config import APP_MODE, PREMIUM_FEATURES
import streamlit as st


# ------------------------------------------
# CHECK PREMIUM ACCESS
# ------------------------------------------

def has_premium_access(feature_name):

    # In beta mode everything unlocked
    if APP_MODE == "beta":
        return True

    # future paid logic here
    user_plan = st.session_state.get("plan", "free")

    if user_plan == "premium":
        return True

    return not PREMIUM_FEATURES.get(feature_name, False)


# ------------------------------------------
# PREMIUM LOCK UI
# ------------------------------------------

def premium_lock():

    st.warning("🔒 Premium Feature")
    st.info(
        "This feature is available in Premium AI Coach plan."
    )
