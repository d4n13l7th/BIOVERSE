"""
Session router for Phase 2 Layer 0.
Endpoints to start, fetch, and update session_state in Supabase.
"""
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from typing import Any
from uuid import uuid4

from supabase_client import supabase

router = APIRouter()


class SessionStartRequest(BaseModel):
    student_id: int
    session_id: str | None = None


@router.post("/start", tags=["Layer0"])
async def start_session(payload: SessionStartRequest):
    """Create a new session_state row in Supabase and return session_id."""
    if supabase is None:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Supabase client not configured")

    session_id = payload.session_id or str(uuid4())
    row = {
        "student_id": payload.student_id,
        "session_id": session_id,
        # other defaults will be handled by DB
    }
    try:
        res = supabase.table("session_state").insert(row).execute()
        if res.error:
            raise HTTPException(status_code=500, detail=str(res.error))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return {"session_id": session_id}


@router.get("/{session_id}", tags=["Layer0"])
async def get_session(session_id: str):
    """Fetch the latest session_state by session_id."""
    if supabase is None:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Supabase client not configured")
    try:
        res = supabase.table("session_state").select("*").eq("session_id", session_id).limit(1).execute()
        if res.error:
            raise HTTPException(status_code=500, detail=str(res.error))
        data = res.data or []
        if len(data) == 0:
            raise HTTPException(status_code=404, detail="session not found")
        return data[0]
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/{session_id}", tags=["Layer0"])
async def update_session(session_id: str, payload: dict[str, Any]):
    """Partial update of session_state for the given session_id. Only provided fields are updated."""
    if supabase is None:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Supabase client not configured")
    if not payload:
        raise HTTPException(status_code=400, detail="empty payload")
    try:
        # set updated_at to server now via DB function
        payload["updated_at"] = "now()"
        # Supabase python client doesn't allow direct SQL expressions easily; use update with provided fields
        res = supabase.table("session_state").update(payload).eq("session_id", session_id).execute()
        if res.error:
            raise HTTPException(status_code=500, detail=str(res.error))
        return {"updated": True}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
