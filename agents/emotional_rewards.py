# =====================================================
# EMOTIONAL REWARD ENGINE
# Positive Reinforcement System
# =====================================================

def emotional_reward_engine(memory):

    memory.setdefault("daily_health_log", [])
    memory.setdefault("emotional_rewards", [])

    logs = memory["daily_health_log"]

    if len(logs) < 2:
        return

    today = logs[-1]
    yesterday = logs[-2]

    rewards = []

    # -----------------------------------
    # ENERGY IMPROVEMENT
    # -----------------------------------
    if today.get("energy", 0) > yesterday.get("energy", 0):
        rewards.append(
            "⚡ Your energy improved today — your habits are working!"
        )

    # -----------------------------------
    # SLEEP IMPROVEMENT
    # -----------------------------------
    if today.get("sleep", 0) > yesterday.get("sleep", 0):
        rewards.append(
            "😴 Better sleep detected. Your body is recovering well."
        )

    # -----------------------------------
    # EXERCISE CONSISTENCY
    # -----------------------------------
    if today.get("exercise"):
        rewards.append(
            "🏃 Great job showing up today — consistency beats perfection!"
        )

    # -----------------------------------
    # HYDRATION SUCCESS
    # -----------------------------------
    if today.get("water", 0) >= 6:
        rewards.append(
            "💧 Hydration goal achieved today. Your body thanks you!"
        )

    # -----------------------------------
    # STREAK CELEBRATION
    # -----------------------------------
    streak = memory.get("streak_days", 0)

    if streak in [3, 5, 7, 10, 14, 21, 30]:
        rewards.append(
            f"🔥 {streak}-day streak! You're building a real health habit."
        )

    memory["emotional_rewards"] = rewards
