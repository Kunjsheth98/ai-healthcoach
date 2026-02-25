from agents.health_score import calculate_health_score
from agents.predictive_burnout_engine import predictive_burnout_core
from agents.life_os_controller import update_life_os_mode
from agents.behavioral_core import detect_behavior_drift
from core.identity_evolution_engine import evolve_identity
from core.attachment_engine import attachment_update

def daily_neural_sync(memory):

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

    # 🧠 SELF CORRECTING BEHAVIOR TRIGGER

    if memory.get("future_projection_state") == "Burnout escalation likely":
        memory["suppression_state"] = "high"

    elif memory.get("future_projection_state") == "Fatigue accumulation risk":
        memory["suppression_state"] = "moderate"

    else:
        memory["suppression_state"] = "none"


    return memory