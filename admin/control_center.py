import streamlit as st
from core.memory import save_memory
from core.budget_guard import get_today_cost
from core.budget_guard import init_budget

# ==========================================
# ADMIN CONTROL CENTER
# ==========================================


def admin_control_center(memory):
    init_budget(memory)
    st.title("🛠️ Admin Control Center")

    # ---------------- AI STATUS ----------------
    st.subheader("🤖 AI System Status")

    if "ai_paused" not in memory:
        memory["ai_paused"] = False

    status = "🔴 PAUSED" if memory["ai_paused"] else "🟢 RUNNING"
    st.write(f"Current Status: **{status}**")

    # Kill switch
    if st.button("⛔ Toggle AI Pause / Resume"):
        memory["ai_paused"] = not memory["ai_paused"]
        save_memory(memory)
        st.rerun()

    st.divider()

    # ---------------- COST MONITOR ----------------
    st.subheader("💰 Cost Monitor")

    today_cost = get_today_cost(memory)
    st.metric("Today's AI Cost ($)", round(today_cost, 3))

    # ---------------- BUDGET CONTROL ----------------
    st.subheader("⚙️ Budget Settings")

    if "admin_budget_limit" not in memory:
        memory["admin_budget_limit"] = 3.0

    new_budget = st.number_input(
        "Daily Budget Limit ($)",
        min_value=0.5,
        max_value=50.0,
        value=float(memory["admin_budget_limit"]),
        step=0.5,
    )

    if st.button("💾 Save Budget"):
        memory["admin_budget_limit"] = new_budget

        # auto resume if new budget allows
        if memory.get("budget", {}).get("daily_cost", 0) < new_budget:
            memory["ai_paused"] = False

        save_memory(memory)
        st.success("Budget updated!")

    st.divider()

    # ---------------- USAGE STATS ----------------
    st.subheader("📊 Usage Stats")

    calls = memory.get("budget", {}).get("ai_calls_today", 0)

    st.metric("AI Calls Today", calls)
