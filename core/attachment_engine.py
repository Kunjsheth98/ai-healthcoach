
# =====================================================
# ATTACHMENT ENGINE
# Builds psychological attachment loop
# =====================================================

def attachment_update(memory):

    memory.setdefault("attachment_score", 0)

    engagement = memory.get("engagement_score", 0)
    streak = memory.get("streak_days", 0)

    attachment = memory["attachment_score"]

    attachment += 0.3 * streak
    attachment += 0.5 * (engagement // 3)

    memory["attachment_score"] = min(round(attachment, 2), 100)