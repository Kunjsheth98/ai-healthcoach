from agents.health_score import calculate_health_score
from agents.predictive_burnout_engine import predictive_burnout_core
from agents.life_os_controller import update_life_os_mode
from agents.behavioral_core import detect_behavior_drift
from core.identity_evolution_engine import evolve_identity
from core.attachment_engine import attachment_update
from core.memory import save_memory
from core.execution_engine import update_execution_score
from core.strategic_focus_engine import update_strategic_focus
from datetime import datetime

def daily_neural_sync(memory):

    today = str(datetime.now().date())

    if memory.get("last_sync_date") == today:
        return memory

    memory["last_sync_date"] = today

    # ===============================
    # 1. Automatic Stress Calculation
    # ===============================

    mood = memory.get("daily_mood", 5)
    sleep = memory.get("sleep_hours", 7)
    energy = memory.get("energy_level", 5)

    # Normalize inputs safely
    mood_factor = (10 - max(1, min(mood, 10))) / 9
    sleep_factor = (7 - max(0, min(sleep, 12))) / 7
    energy_factor = (10 - max(1, min(energy, 10))) / 9

    # Weighted normalized stress (0–1 scale)
    stress_raw = (
        mood_factor * 0.4 +
        sleep_factor * 0.4 +
        energy_factor * 0.2
    )

    # Convert to 0–10 scale
    stress = round(stress_raw * 10)

    memory["stress_index"] = max(0, min(10, stress))

    memory["stress_index"] = max(0, min(10, round(stress)))

    # ===============================
    # 2. Mental Score
    # ===============================

    memory["mental_score"] = max(
        0,
        min(100, 60 - (memory["stress_index"] * 5) + mood * 2)
    )
    memory.setdefault("mental_history", [])
    memory["mental_history"].append({
        "stress_index": memory["stress_index"],
        "mental_score": memory["mental_score"]
    })

    # ===============================
    # 3️⃣ Sleep Debt Accumulation
    # ===============================

    sleep = memory.get("sleep_hours", 7)
    sleep_debt = memory.get("sleep_debt", 0)

    # Ideal sleep baseline = 7 hours
    if sleep < 7:
        sleep_debt += (7 - sleep) * 2   # accumulate faster
    else:
        sleep_debt = max(0, sleep_debt - 3)  # recover slowly

    memory["sleep_debt"] = min(100, sleep_debt)

    # Keep only last 30 entries
    memory["mental_history"] = memory["mental_history"][-30:]

    # ===============================
    # 4. Recalculate Health Score
    # ===============================

    calculate_health_score(memory)
    update_life_os_mode(memory)

    memory.setdefault("health_score_history", [])
    memory["health_score_history"].append(memory.get("health_score", 50))

    # keep last 60 days
    memory["health_score_history"] = memory["health_score_history"][-60:]
    # ===============================
    # 5. Run Predictive Engine
    # ===============================
    predictive_burnout_core(memory)

    # ===============================
    # 🔥 Sleep Debt → Burnout Amplifier
    # ===============================

    sleep_debt = memory.get("sleep_debt", 0)
    burnout = memory.get("burnout_risk_level", 0)

    # Every 15 debt points adds +1 burnout
    burnout += int(sleep_debt / 15)

    memory["burnout_risk_level"] = min(100, burnout)

    # -------- ADVANCED STRESS ENGINE --------

    sleep_hours = memory.get("sleep_hours", 0)
    energy = memory.get("energy_level", 5)
    water = memory.get("water_intake", 0)
    discipline = memory.get("lifestyle", {}).get("discipline_score", 5)
    sleep_pattern = memory.get("lifestyle", {}).get("sleep_pattern", "regular")
    activity_type = memory.get("lifestyle", {}).get("activity_type", "moderate")
    emotion = memory.get("emotion_state", "stable")
    burnout = memory.get("burnout_risk_level", 0)

    # Normalize
    sleep_score = min(sleep_hours / 7, 1)
    hydration_score = min(water / 8, 1)
    energy_score = energy / 10
    discipline_score = discipline / 10

    stress_score = (
        (1 - sleep_score) * 0.30 +
        (1 - hydration_score) * 0.15 +
        (1 - energy_score) * 0.20 +
        (1 - discipline_score) * 0.10
    )

    # Add lifestyle penalties
    if sleep_pattern == "irregular":
        stress_score += 0.10

    if activity_type == "desk":
        stress_score += 0.05

    # Emotional multiplier
    if emotion in ["anxious", "low", "overwhelmed"]:
        stress_score += 0.10

    # Burnout amplification
    stress_score += burnout / 200

    stress_score = round(min(stress_score, 1), 2)

    memory["stress_score"] = stress_score

    # Nervous system classification
    if stress_score > 0.75:
        memory["system_state"] = "overloaded"
    elif stress_score > 0.45:
        memory["system_state"] = "recovery"
    else:
        memory["system_state"] = "growth"

    evolve_identity(memory)
    attachment_update(memory)

    # ⚡ REFLEX PRIORITY ESCALATION
    if memory.get("reflex_alert"):
        memory["brain_state"] = {
            "mode": "recovery_lock",
            "intervention": "force_recovery"
    }

    if memory.get("burnout_risk_level", 0) >= 7:
        memory["brain_state"] = {
            "mode": "recovery_lock",
            "intervention": "force_recovery"
        }

    elif memory.get("goal_mode") == "muscle_gain" and memory.get("burnout_risk_level", 0) < 4:
        memory["brain_state"] = {
            "mode": "performance",
            "intervention": "normal"
        }
    # 🔮 STORE BURNOUT PROBABILITY HISTORY

    memory.setdefault("burnout_probability_history", [])

    prob = memory.get("risk_forecast", {}).get("burnout_probability", 0)

    memory["burnout_probability_history"].append(prob)

    # keep last 30 days
    memory["burnout_probability_history"] = memory["burnout_probability_history"][-30:]    
    
    detect_behavior_drift(memory)

    # 🚨 RELAPSE INTERCEPTION PROTOCOL

    if memory.get("behavior_drift") and memory.get("streak_days", 0) >= 3:
        memory["relapse_risk"] = True
    else:
        memory["relapse_risk"] = False

    # 🧠 PROMPT PERFORMANCE ANALYSIS

    scores = memory.get("response_scores", [])

    if len(scores) >= 10:
        avg_score = sum(scores[-10:]) / 10

        memory.setdefault("prompt_performance", {})

        current_style = memory.get("adaptive_coach_style", "supportive")

        memory["prompt_performance"][current_style] = avg_score

    # 🔄 AUTO STYLE OPTIMIZATION

    performance = memory.get("prompt_performance", {})

    if performance:
        best_style = max(performance, key=performance.get)
        memory["active_prompt_style"] = best_style

    # 🧬 AUTONOMOUS EVOLUTION STAGE ENGINE

    memory.setdefault("evolution_stage", 1)

    streak = memory.get("streak_days", 0)
    confidence = memory.get("risk_confidence_score", 50)

    if streak >= 7 and confidence > 60:
        memory["evolution_stage"] = 2

    if streak >= 21 and confidence > 70:
        memory["evolution_stage"] = 3

    if streak >= 45 and confidence > 80:
        memory["evolution_stage"] = 4

    # =====================================================
    # 🧬 IDENTITY STABILITY EVOLUTION
    # =====================================================

    memory.setdefault("identity_stability", 0)

    streak = memory.get("streak_days", 0)
    engagement = memory.get("engagement_score", 0)
    relapse = memory.get("relapse_risk", False)

    stability = memory["identity_stability"]

    # Increase stability with consistency
    if streak >= 3 and not relapse:
        stability += 1

    # Engagement bonus
    if engagement > 5:
        stability += 1

    # Reduce if relapse
    if relapse:
        stability = max(0, stability - 2)

    memory["identity_stability"] = min(100, stability)

    # =====================================================
    # 🧠 IDENTITY MATURITY STAGE
    # =====================================================

    stability = memory.get("identity_stability", 0)

    if stability >= 30:
        memory["identity_maturity"] = "emerging"

    if stability >= 60:
        memory["identity_maturity"] = "solid"

    if stability >= 85:
        memory["identity_maturity"] = "integrated"

    if stability < 30:
        memory["identity_maturity"] = "forming"

    # 🧠 COACHING STYLE MUTATION

    stage = memory.get("evolution_stage", 1)

    if stage == 1:
        memory["adaptive_coach_style"] = "supportive"

    elif stage == 2:
        memory["adaptive_coach_style"] = "accountability"

    elif stage == 3:
        memory["adaptive_coach_style"] = "performance"

    elif stage >= 4:
        memory["adaptive_coach_style"] = "elite"

    # 🚀 IDENTITY UPGRADE TRIGGER

    if memory.get("evolution_stage", 1) >= 3:
        memory.setdefault("identity_lock", {})
        memory["identity_lock"]["evolved"] = True    

    # 🎯 ADAPTIVE DIFFICULTY SCALING

    if memory.get("adaptive_coach_style") == "performance":
        memory["difficulty_modifier"] = 1.1

    elif memory.get("adaptive_coach_style") == "elite":
        memory["difficulty_modifier"] = 1.2

    else:
        memory["difficulty_modifier"] = 1.0    

    # 📊 RISK CONFIDENCE CURVE

    burnout = memory.get("burnout_risk_level", 0)
    momentum = memory.get("burnout_momentum", 0)

    confidence_curve = max(0, 100 - (burnout * 8) - (momentum * 5))

    # ------------------------------
    # 🧬 Body Fat Influence Engine
    # ------------------------------

    bf_history = memory.get("body_fat_history", [])

    if len(bf_history) >= 14:
        last_7 = sum(bf_history[-7:]) / 7
        prev_7 = sum(bf_history[-14:-7]) / 7
        bf_trend = round(last_7 - prev_7, 2)
    else:
        bf_trend = 0

    memory["body_fat_trend_7d"] = bf_trend

    # If cutting fat → reward confidence
    if bf_trend < -0.2:
        confidence_curve += 5

    # If gaining fat fast → slow evolution
    elif bf_trend > 0.3:
        confidence_curve -= 5

    confidence_curve = min(100, max(0, confidence_curve))

    memory["risk_confidence_score"] = round(confidence_curve, 2)

    # 🔮 7-DAY FUTURE STATE PROJECTION

    sleep = memory.get("sleep_hours", 7)
    energy = memory.get("energy_level", 5)
    trend = memory.get("mental_pattern", "stable")

    projection_score = sleep + energy

    if trend == "stress_increasing":
        projection_score -= 3

    if memory.get("burnout_risk_level", 0) >= 7:
        future_state = "Burnout escalation likely"
    elif projection_score >= 12:
        future_state = "Energy resilience improving"
    elif projection_score >= 8:
        future_state = "Stable but vulnerable"
    else:
        future_state = "Fatigue accumulation risk"

    memory["future_projection_state"] = future_state

    # ===============================
    # 🧠 BODY FAT ESTIMATION ENGINE
    # ===============================

    # Get body data
    profile = memory.get("profile", {})
    weight = profile.get("weight_kg")
    waist = profile.get("waist_cm")

    height = profile.get("height_cm", 170)

    if weight and waist and height:
        # Improved BMI-based proxy
        bmi = weight / ((height / 100) ** 2)
        bf_est = (1.2 * bmi) + (0.23 * 30) - 5.4
    else:
        bf_est = memory.get("body_fat_estimate", 20)
        
    # ===============================
    # 💪 MUSCLE GAIN ESTIMATOR
    # ===============================

    goal = memory.get("goal_mode", "general")
    weight_trend = memory.get("weight_trend_7d", 0)
    intensity = memory.get("global_intensity_level", "moderate")

    muscle_gain_score = memory.get("muscle_gain_score", 0)

    if goal == "muscle_gain" and intensity == "high":
        if weight_trend > 0:
            muscle_gain_score += 1

    if goal == "fat_loss" and weight_trend < 0:
        muscle_gain_score += 0.5

    memory["muscle_gain_score"] = round(muscle_gain_score, 2)  

    # ===============================
    # 🧬 HORMONAL STRESS INDEX
    # ===============================

    sleep_debt = memory.get("sleep_debt", 0)
    burnout = memory.get("burnout_risk_level", 0)
    stress = memory.get("stress_score", 0)
    heavy = memory.get("heavy_session_count", 0)

    hormonal_stress = (
        sleep_debt * 0.2 +
        burnout * 1.5 +
        stress * 50 +
        heavy * 5
    )

    hormonal_stress = min(100, round(hormonal_stress, 2))
    memory["hormonal_stress_index"] = hormonal_stress 

    # Adaptive correction based on calorie vs intake
    calorie_target = memory.get("daily_calorie_target", weight * 30)
    # last 7 days intake (if available)
    weekly_log = memory.get("daily_food_log", [])[-7:]
    if weekly_log:
        avg_intake = sum(d.get("calories",0) for d in weekly_log) / len(weekly_log)
        diff = avg_intake - calorie_target
        # if consistent surplus → body fat ↑ slightly
        if diff > 200:
            bf_est += 0.2
        # if consistent deficit → body fat ↓ slightly
        elif diff < -200:
            bf_est -= 0.2

    # clamp estimate
    bf_est = max(5, min(bf_est, 50))

    memory["body_fat_estimate"] = round(bf_est, 2)

    # history
    memory.setdefault("body_fat_history", [])
    memory["body_fat_history"].append(memory["body_fat_estimate"])
    memory["body_fat_history"] = memory["body_fat_history"][-60:]

    # ===============================
    # ⚖️ WEIGHT TREND ENGINE
    # ===============================

    profile = memory.get("profile", {})
    weight = profile.get("weight_kg")

    if weight:
        memory.setdefault("weight_history", [])
        memory["weight_history"].append(weight)
        memory["weight_history"] = memory["weight_history"][-60:]

    # Calculate 7-day smoothed trend
    weights = memory.get("weight_history", [])

    if len(weights) >= 7:
        last_7_avg = sum(weights[-7:]) / 7
        prev_7_avg = sum(weights[-14:-7]) / 7 if len(weights) >= 14 else last_7_avg

        trend_diff = round(last_7_avg - prev_7_avg, 2)
        memory["weight_trend_7d"] = trend_diff
    else:
        memory["weight_trend_7d"] = 0   

    # ===============================
    # 🔥 Adaptive Calorie Regulation
    # ===============================

    weight_trend = memory.get("weight_trend_7d", 0)
    current_target = memory.get("daily_calorie_target", None)

    profile = memory.get("profile", {})
    weight = profile.get("weight_kg")

    if weight:
        # Base calorie formula
        base_target = weight * 30

        if not current_target:
            current_target = base_target

        # If gaining too fast → reduce slightly
        if weight_trend > 0.4:
            current_target -= 100

        # If losing too fast → increase slightly
        elif weight_trend < -0.5:
            current_target += 100

        # Keep safe bounds
        min_target = weight * 22
        max_target = weight * 40

        current_target = max(min_target, min(max_target, current_target))

        memory["daily_calorie_target"] = round(current_target) 

    # ===============================
    # 🧬 Hormonal Stress Adjustment
    # ===============================

    hormonal_stress = memory.get("hormonal_stress_index", 0)
    calorie_target = memory.get("daily_calorie_target")

    if calorie_target:

        # If high stress → prioritize recovery
        if hormonal_stress > 75:
            calorie_target -= 100

        # If extremely low stress + growth mode → slight boost
        elif hormonal_stress < 30 and memory.get("life_os_mode") == "performance":
            calorie_target += 50

        # Safe bounds again
        weight = profile.get("weight_kg")
        if weight:
            min_target = weight * 22
            max_target = weight * 40
            calorie_target = max(min_target, min(max_target, calorie_target))

        memory["daily_calorie_target"] = round(calorie_target)    

    # 🧠 META-BRAIN SCENARIO SIMULATION

    sleep = memory.get("sleep_hours", 7)
    energy = memory.get("energy_level", 5)
    burnout = memory.get("burnout_risk_level", 0)

    # Simulated trajectories
    continue_path = burnout + 1
    improve_sleep_path = burnout - 2
    reduce_training_path = burnout - 1

    # Choose optimal path
    best_projection = min(continue_path, improve_sleep_path, reduce_training_path)

    if best_projection == improve_sleep_path:
        memory["meta_strategy"] = "prioritize_sleep"

    elif best_projection == reduce_training_path:
        memory["meta_strategy"] = "reduce_intensity"

    else:
        memory["meta_strategy"] = "maintain_path"

    # 🛡 META STRATEGIC OVERRIDE

    if memory.get("meta_strategy") == "prioritize_sleep":
        memory["brain_state"] = {
            "mode": "recovery_lock",
            "intervention": "force_recovery"
        }

    elif memory.get("meta_strategy") == "reduce_intensity":
        memory["brain_state"] = {
            "mode": "resilience",
            "intervention": "intensity_reduction"
        }    

    # =====================================================
    # 🌍 GLOBAL INTENSITY ENGINE (Single Source of Truth)
    # =====================================================

    burnout = memory.get("burnout_risk_level", 0)
    sleep = memory.get("sleep_hours", 7)
    sleep_debt = memory.get("sleep_debt", 0)
    system_state = memory.get("system_state", "balanced")
    meta = memory.get("meta_strategy")

    global_intensity = "moderate"

    # Hard recovery conditions
    if burnout >= 8 or sleep < 5 or sleep_debt > 40:
        global_intensity = "very_light"

    # Recovery bias
    elif system_state == "overloaded":
        global_intensity = "very_light"

    elif meta == "prioritize_sleep":
        global_intensity = "very_light"

    elif meta == "reduce_intensity":
        global_intensity = "moderate"

    # High performance unlock
    elif burnout <= 3 and sleep >= 7 and sleep_debt < 10:
        global_intensity = "high"

    else:
        global_intensity = "moderate"

    memory["global_intensity_level"] = global_intensity    

    # ---- Companion Feedback ----
    insight = ""

    if memory.get("primary_intent") == "sleep":
        insight = "Sleep consistency is your focus. Small improvements daily."

    elif memory.get("primary_intent") == "stress":
        insight = "Energy recovery matters more than intensity today."

    elif memory.get("primary_intent") == "movement":
        insight = "Consistency beats intensity. Keep moving lightly."

    # -------- STRESS INTERVENTION ENGINE --------

    intervention = None

    if memory["system_state"] == "overloaded":
        intervention = "Full recovery protocol: No intense work. 20 min slow walk. Early sleep. Hydrate aggressively."

    elif memory["system_state"] == "recovery":
        intervention = "Moderate workload. 10 min breathwork. Light yoga. No late-night screen exposure."

    elif memory["system_state"] == "growth":
        intervention = "High performance supported. Structured deep work + strength session recommended."

    memory["system_intervention"] = intervention

    memory["daily_companion_insight"] = insight
    update_execution_score(memory)
    update_strategic_focus(memory)

    # 🔥 GLOBAL INTENSITY CALCULATION
    sleep = memory.get("sleep_hours", 7)
    burnout = memory.get("burnout_risk_level", 0)
    emotional_depth = memory.get("emotional_depth_level", "low")
    execution_score = memory.get("execution_score", 50)
    heavy = memory.get("heavy_session_count", 0)
    energy = memory.get("energy_level", 5)

    intensity_score = (
        (energy * 2)
        - (burnout * 1.5)
        - (heavy * 5)
        - (memory.get("sleep_debt", 0) * 0.3)
    )

    if intensity_score <= 5:
        memory["global_intensity_level"] = "very_light"
    elif intensity_score <= 12:
        memory["global_intensity_level"] = "moderate"
    else:
        memory["global_intensity_level"] = "high"

    # Emotional softness bias
    if emotional_depth == "high":
        global_intensity = "very_light"

    # Performance reliability boost
    if execution_score > 70 and burnout <= 4:
        global_intensity = "high"    

    # 🔥 ADAPTIVE CALORIE TARGET ENGINE
    weight = memory.get("profile", {}).get("weight_kg", 70)
    goal = memory.get("goal_mode", "general")
    global_intensity = memory.get("global_intensity_level", "moderate")

    # Base maintenance estimate
    maintenance = weight * 30

    if goal == "fat_loss":
        target = maintenance - 400
    elif goal == "muscle_gain":
        target = maintenance + 300
    else:
        target = maintenance

    # Intensity modulation
    if global_intensity == "very_light":
        target -= 100   # recovery day slight reduction
    elif global_intensity == "high":
        target += 150   # performance support

    memory["daily_calorie_target"] = int(target)  

    # 🔄 WEEKLY CALORIE CORRECTION ENGINE

    food_log = memory.get("daily_food_log", [])
    calorie_target = memory.get("daily_calorie_target", target)

    if len(food_log) >= 7:
        last_7 = food_log[-7:]
        avg_intake = sum(d.get("calories", 0) for d in last_7) / 7

        deviation = avg_intake - calorie_target

        # Only adjust if deviation meaningful (>150 kcal)
        if abs(deviation) > 150:

            # Fat loss logic
            if goal == "fat_loss":
                if deviation > 0:
                    calorie_target -= 100  # tighten deficit
                else:
                    calorie_target += 100  # avoid excessive deficit

            # Muscle gain logic
            elif goal == "muscle_gain":
                if deviation > 0:
                    calorie_target -= 100  # reduce excess fat gain
                else:
                    calorie_target += 100  # increase support

            memory["daily_calorie_target"] = int(calorie_target)
            memory["weekly_calorie_adjustment"] = True
        else:
            memory["weekly_calorie_adjustment"] = False  

    save_memory(memory)
    return memory
