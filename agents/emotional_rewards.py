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
        rewards.append("⚡ Your energy improved today — your habits are working!")

    # -----------------------------------
    # SLEEP IMPROVEMENT
    # -----------------------------------
    if today.get("sleep", 0) > yesterday.get("sleep", 0):
        rewards.append("😴 Better sleep detected. Your body is recovering well.")

    # -----------------------------------
    # EXERCISE CONSISTENCY
    # -----------------------------------
    exercise_days_last3 = sum(
        1 for d in logs[-3:] if d.get("exercise")
    )

    if exercise_days_last3 >= 2:
        rewards.append("🏃 Exercise consistency building — keep pushing!")

    # -----------------------------------
    # HYDRATION SUCCESS
    # -----------------------------------
    weight = memory.get("profile", {}).get("weight_kg", 60)
    hydration_target = max(6, int(weight / 10))

    if today.get("water", 0) >= hydration_target:
        rewards.append("💧 Hydration goal achieved today. Your body thanks you!")

    # -----------------------------------
    # STREAK CELEBRATION
    # -----------------------------------
    streak = memory.get("streak_days", 0)

    if streak in [3, 5, 7, 10, 14, 21, 30]:
        rewards.append(f"🔥 {streak}-day streak! You're building a real health habit.")

    # Prevent duplicate rewards for same day
    last_reward_date = memory.get("last_reward_date")

    from datetime import date
    today_date = str(date.today())

    if last_reward_date != today_date:
        memory["emotional_rewards"] = rewards
        memory["last_reward_date"] = today_date
