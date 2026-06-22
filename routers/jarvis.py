"""
Routers for Jarvis VUI (Layer 1).

Provides a simple FSM that matches transcript to materi entries
and returns a JarvisQueryResponse. Uses Supabase via supabase_client.
"""
from fastapi import APIRouter, HTTPException, status
from typing import Optional
from pydantic import BaseModel

import models
from supabase_client import supabase
from datetime import datetime

router = APIRouter()


class JarvisStateMachine:
    """Simple finite state machine for Jarvis VUI transitions."""

    def __init__(self, session_row: dict | None):
        self.session = session_row or {}

    def determine_state_and_response(self, transcript: str, materi_row: Optional[dict], deps: list[dict]):
        """Return (state, response_text, materi_content)

        - materi_row present -> either TOPIC_VALID_IN_SCOPE or TOPIC_AHEAD_OF_LEVEL depending on deps
        - materi_row missing -> TOPIC_UNKNOWN
        """
        if not materi_row:
            return models.JarvisState.TOPIC_UNKNOWN, "Maaf, saya tidak menemukan topik itu. Bisa ulangi atau sebutkan kata lain?", None

        topic_id = materi_row.get("id")
        # If there are no prerequisites, topic is valid
        if not deps:
            text = materi_row.get("deskripsi") or f"Kita akan belajar tentang {materi_row.get('judul')}."
            return models.JarvisState.TOPIC_VALID_IN_SCOPE, text, materi_row

        # There are prerequisites — check minimal condition: whether current_topic_id matches a prereq
        current_topic_id = self.session.get("current_topic_id")
        prereq_ids = [d.get("prerequisite_topic_id") for d in deps if d.get("prerequisite_topic_id")]
        if current_topic_id and current_topic_id in prereq_ids:
            text = materi_row.get("deskripsi") or f"Kita akan belajar tentang {materi_row.get('judul')}."
            return models.JarvisState.TOPIC_VALID_IN_SCOPE, text, materi_row

        # Otherwise it's ahead of level — use connecting_fact from first dependency
        connecting_fact = deps[0].get("connecting_fact") or "topik ini membutuhkan prasyarat sebelumnya"
        current_topic_title = "materi yang sedang dikerjakan"
        if self.session.get("current_topic_id"):
            # try to fetch current topic title
            try:
                cur = supabase.table("materi").select("judul").eq("id", self.session.get("current_topic_id")).limit(1).execute()
                if cur.data and len(cur.data) > 0:
                    current_topic_title = cur.data[0].get("judul")
            except Exception:
                pass

        template = (
            f"{materi_row.get('judul')} itu menarik! Tapi sebelum ke sana, ayo selesaikan {current_topic_title} dulu — karena {connecting_fact}. Mau lanjut?"
        )
        return models.JarvisState.TOPIC_AHEAD_OF_LEVEL, template, None


@router.post("/query", tags=["Layer1"])  
async def jarvis_query(payload: models.JarvisQueryRequest):
    """Handle voice transcript from client, run simple NLU (keyword matching),
    run FSM, log interaction, and update session_state.
    """
    if supabase is None:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Supabase client not configured")

    # Fetch session_state
    try:
        s = supabase.table("session_state").select("*").eq("session_id", payload.session_id).limit(1).execute()
        if s.error:
            raise HTTPException(status_code=500, detail=str(s.error))
        session_row = s.data[0] if (s.data and len(s.data) > 0) else None
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    # Simple NLU: try matching materi.judul or materi.deskripsi using ilike on judul then deskripsi
    transcript = (payload.transcript or "").strip()
    materi_row = None
    try:
        if transcript:
            q = supabase.table("materi").select("*").ilike("judul", f"%{transcript}%").limit(1).execute()
            if q.data and len(q.data) > 0:
                materi_row = q.data[0]
            else:
                q2 = supabase.table("materi").select("*").ilike("deskripsi", f"%{transcript}%").limit(1).execute()
                if q2.data and len(q2.data) > 0:
                    materi_row = q2.data[0]
    except Exception:
        # Fallback: ignore search errors and treat as unknown
        materi_row = None

    # Fetch dependencies for the matched topic if any
    deps = []
    if materi_row:
        try:
            deps_res = supabase.table("topic_dependency_graph").select("*").eq("topic_id", materi_row.get("id")).execute()
            deps = deps_res.data or []
        except Exception:
            deps = []

    fsm = JarvisStateMachine(session_row)
    state, response_text, materi_content = fsm.determine_state_and_response(transcript, materi_row, deps)

    # Log interaction
    try:
        log_row = {
            "student_id": payload.student_id,
            "session_id": payload.session_id,
            "event_type": "voice_query",
            "payload": {"transcript": transcript, "matched_topic": materi_row.get('judul') if materi_row else None, "state": state}
        }
        supabase.table("interaction_log").insert(log_row).execute()
    except Exception:
        pass

    # Update session_state: fsm_state, last_query, last_topic_attempted
    try:
        update_payload = {
            "fsm_state": state.value if hasattr(state, 'value') else str(state),
            "last_query": transcript,
            "last_topic_attempted": materi_row.get('judul') if materi_row else None,
            "updated_at": datetime.utcnow().isoformat()
        }
        supabase.table("session_state").update(update_payload).eq("session_id", payload.session_id).execute()
    except Exception:
        pass

    return models.JarvisQueryResponse(
        response_text=response_text,
        action=None,
        fsm_state=state,
        materi_content=materi_content
    )
