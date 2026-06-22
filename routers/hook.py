"""
Hook router for Phase 2 Layer 2.
Endpoints for idle detection, reward gating, and reward claiming.
All Hook logic gates on hook_enabled flag (default FALSE).
"""
from fastapi import APIRouter, HTTPException, status
from datetime import datetime, timedelta

import models
from supabase_client import supabase

router = APIRouter()


@router.post("/idle-event", tags=["Layer2"])
async def handle_idle_event(payload: models.HookIdleEvent):
    """
    Handle idle event from client.
    Checks hook_enabled — if FALSE, returns skipped response.
    If TRUE: updates engagement_score, detects escalation level.
    """
    if supabase is None:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Supabase client not configured")

    try:
        # Fetch session_state
        s = supabase.table("session_state").select("*").eq("session_id", payload.session_id).limit(1).execute()
        if s.error:
            raise HTTPException(status_code=500, detail=str(s.error))
        session_row = s.data[0] if (s.data and len(s.data) > 0) else None
        if not session_row:
            raise HTTPException(status_code=404, detail="session not found")

        # GATE: hook_enabled must be TRUE to proceed with Hook logic
        if not session_row.get("hook_enabled", False):
            return models.HookIdleResponse(escalation_level=0, should_notify_caregiver=False)

        # Hook is enabled — process idle event
        idle_secs = payload.idle_duration
        threshold = session_row.get("hook_idle_threshold_seconds", 180)
        
        # Determine escalation level based on idle duration
        escalation_level = 1
        should_notify = False
        if idle_secs >= threshold + 240:  # Stage 3
            escalation_level = 3
            should_notify = True
        elif idle_secs >= threshold + 120:  # Stage 2
            escalation_level = 2
        elif idle_secs >= threshold:  # Stage 1
            escalation_level = 1

        # Update engagement_score (decreased by idle duration)
        current_engagement = session_row.get("engagement_score", 100.0)
        new_engagement = max(0, current_engagement - (idle_secs / 60.0) * 5)  # rough formula
        
        update_payload = {
            "engagement_score": new_engagement,
            "updated_at": datetime.utcnow().isoformat()
        }
        supabase.table("session_state").update(update_payload).eq("session_id", payload.session_id).execute()

        # Log interaction
        try:
            log_row = {
                "student_id": payload.student_id,
                "session_id": payload.session_id,
                "event_type": "idle_event",
                "payload": {
                    "idle_duration": idle_secs,
                    "escalation_level": escalation_level,
                    "current_screen": payload.current_screen
                }
            }
            supabase.table("interaction_log").insert(log_row).execute()
        except Exception:
            pass

        return models.HookIdleResponse(
            escalation_level=escalation_level,
            should_notify_caregiver=should_notify
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/reward-status/{student_id}", tags=["Layer2"])
async def get_reward_status(student_id: int):
    """
    Fetch reward gate status for a student.
    Returns current_task_status and reward_expires_at from session_state.
    Client must check reward_expires_at against server time (NEVER use client-side timer).
    """
    if supabase is None:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Supabase client not configured")

    try:
        # Fetch latest session for this student
        s = supabase.table("session_state").select("*").eq("student_id", student_id).order("created_at", desc=True).limit(1).execute()
        if s.error:
            raise HTTPException(status_code=500, detail=str(s.error))
        session_row = s.data[0] if (s.data and len(s.data) > 0) else None
        if not session_row:
            raise HTTPException(status_code=404, detail="no active session for student")

        return models.RewardGateStatus(
            student_id=student_id,
            current_task_status=session_row.get("current_task_status", "in_progress"),
            reward_expires_at=session_row.get("reward_expires_at"),
            interaction_budget_seconds=session_row.get("interaction_budget_seconds", 60)
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/reward-claim", tags=["Layer2"])
async def claim_reward(payload: models.RewardClaimRequest):
    """
    Claim a reward after task is complete.
    Sets reward_expires_at = now() + interaction_budget_seconds.
    Sets current_task_status = 'reward_unlocked'.
    """
    if supabase is None:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Supabase client not configured")

    try:
        # Fetch session
        s = supabase.table("session_state").select("*").eq("session_id", payload.session_id).limit(1).execute()
        if s.error:
            raise HTTPException(status_code=500, detail=str(s.error))
        session_row = s.data[0] if (s.data and len(s.data) > 0) else None
        if not session_row:
            raise HTTPException(status_code=404, detail="session not found")

        # Validate task status
        if session_row.get("current_task_status") != "completed_pending_reward":
            raise HTTPException(status_code=400, detail="task is not ready to claim reward")

        # Calculate reward expiry: now + budget seconds
        budget_secs = session_row.get("interaction_budget_seconds", 60)
        now = datetime.utcnow()
        expires_at = now + timedelta(seconds=budget_secs)

        # Update session_state
        update_payload = {
            "reward_expires_at": expires_at.isoformat(),
            "current_task_status": "reward_unlocked",
            "updated_at": now.isoformat()
        }
        supabase.table("session_state").update(update_payload).eq("session_id", payload.session_id).execute()

        # Log interaction
        try:
            log_row = {
                "student_id": payload.student_id,
                "session_id": payload.session_id,
                "event_type": "reward_claimed",
                "payload": {
                    "expires_at": expires_at.isoformat()
                }
            }
            supabase.table("interaction_log").insert(log_row).execute()
        except Exception:
            pass

        return models.RewardGateStatus(
            student_id=payload.student_id,
            current_task_status="reward_unlocked",
            reward_expires_at=expires_at,
            interaction_budget_seconds=budget_secs
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
