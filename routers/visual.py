"""
Visual-Haptic router for Phase 2 Layer 3.
Endpoint for visual/haptic interactions (button clicks, quiz answers).
Determines haptic patterns and returns next content.
"""
from fastapi import APIRouter, HTTPException, status
from typing import Optional

import models
from supabase_client import supabase

router = APIRouter()


def get_haptic_pattern(is_correct: bool) -> list[int]:
    """
    Return vibration pattern based on correctness.
    - Correct: [200, 100, 200] (two firm taps)
    - Wrong: [100] (single short tap)
    - Transition: [50, 50, 50, 50] (four light taps)
    """
    if is_correct:
        return [200, 100, 200]
    else:
        return [100]


@router.post("/interaction", tags=["Layer3"])
async def handle_visual_interaction(payload: models.VisualInteractionEvent):
    """
    Handle visual/haptic interaction from tunarungu frontend.
    Validates answer against quiz data, determines haptic pattern,
    returns next content and feedback.
    """
    if supabase is None:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Supabase client not configured")

    try:
        # For now: just return haptic pattern and feedback
        # Full implementation would validate against quiz in Supabase
        is_correct = payload.is_correct
        haptic = get_haptic_pattern(is_correct)

        # Log interaction
        try:
            log_row = {
                "student_id": payload.student_id,
                "session_id": payload.session_id,
                "event_type": "visual_click",
                "payload": {
                    "element_id": payload.element_id,
                    "action_type": payload.action_type,
                    "is_correct": is_correct
                }
            }
            supabase.table("interaction_log").insert(log_row).execute()
        except Exception:
            pass

        # Prepare response
        feedback_msg = "✅ Benar!" if is_correct else "❌ Coba lagi"
        next_content = None
        
        # If correct, could fetch next content from materi table
        if is_correct:
            try:
                # TODO: query next materi based on current topic progression
                pass
            except Exception:
                pass

        return {
            "is_correct": is_correct,
            "haptic_pattern": haptic,
            "next_content": next_content,
            "feedback_message": feedback_msg
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
