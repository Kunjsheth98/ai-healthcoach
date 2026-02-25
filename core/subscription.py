from core.app_config import APP_MODE, PREMIUM_FEATURES
import streamlit as st

# ------------------------------------------
# CHECK PREMIUM ACCESS
# ------------------------------------------


def has_premium_access(feature_name):

    # Beta mode → everything unlocked
    if APP_MODE == "beta":
        return True

    user_plan = st.session_state.get("plan", "free")

    # Premium users get everything
    if user_plan == "premium":
        return True

    # Free users: only access if feature is NOT marked premium
    is_premium_feature = PREMIUM_FEATURES.get(feature_name, False)

    return not is_premium_feature


# ------------------------------------------
# PREMIUM LOCK UI
# ------------------------------------------


def premium_lock():

    st.warning("🔒 Premium Feature")
    st.info("This feature is available in Premium AI Coach plan.")
