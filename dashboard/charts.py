import matplotlib.pyplot as plt
import streamlit as st


def show_health_chart(memory):

    scores = memory.get("health_score_history", [])

    if not scores:
        st.info("No historical data yet.")
        return

    fig, ax = plt.subplots()
    ax.plot(scores, label="Health Score Trend")
    burnout_probs = memory.get("burnout_probability_history", [])

    if burnout_probs:
        ax.plot(burnout_probs, label="Burnout Probability Trend")
    ax.legend()

    st.pyplot(fig)
