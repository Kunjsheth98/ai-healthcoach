import matplotlib.pyplot as plt
import streamlit as st


def show_health_chart(memory):

    scores = [memory["health_score"]] * 7
    water = [memory["water_intake"]] * 7

    fig, ax = plt.subplots()
    ax.plot(scores, label="Health Score")
    ax.plot(water, label="Water Intake")
    ax.legend()

    st.pyplot(fig)
