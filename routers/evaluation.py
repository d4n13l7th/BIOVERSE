"""
Bioverse - Evaluation Routes
===============================
Endpoint evaluasi kuis yang menjalankan adaptive rules engine.
Menggantikan POST /api/evaluate dari adaptive_engine/main.py
dan EvaluationController.php (Laravel).
"""

from fastapi import APIRouter, HTTPException
from datetime import datetime

from models import EvaluationRequest, AdaptiveRecommendation, ProgressRecord
from rules_logic import AdaptiveRulesEngine
from database import add_progress, get_progress

router = APIRouter(prefix="/api", tags=["Evaluation"])

# Inisialisasi rules engine
rules_engine = AdaptiveRulesEngine()


@router.post("/evaluate", response_model=AdaptiveRecommendation)
async def evaluate_student(request: EvaluationRequest):
    """
    Menerima data evaluasi siswa dari frontend (quiz.js),
    menjalankan logika adaptif, dan mengembalikan rekomendasi.

    Flow:
    1. Frontend mengirim skor + response_time
    2. Engine menganalisis tren historis
    3. Engine menentukan aksi (increase/decrease/maintain)
    4. Rekomendasi dikirim balik ke frontend
    5. Frontend mengupdate UI (speed, level, feedback)
    """
    try:
        # Jalankan adaptive rules engine
        recommendation = rules_engine.process(
            student_id=request.student_id,
            module=request.module,
            score=request.score,
            response_time=request.response_time,
            history=[h.model_dump() for h in request.history],
        )

        # Simpan progress record
        progress_record = ProgressRecord(
            student_id=request.student_id,
            module_id=0,  # TODO: map module name to ID
            module=request.module,
            score=request.score,
            response_time=request.response_time,
            interactions={},
            evaluated_at=datetime.now().isoformat(),
        )
        add_progress(progress_record)

        # Update level in Supabase if needed
        new_level = recommendation.get("new_level")
        if new_level is not None and new_level != request.current_level:
            try:
                from supabase_client import supabase
                if supabase:
                    supabase.table('abk_profiles').update({'default_level': new_level}).eq('id', request.student_id).execute()
            except Exception as e:
                print(f"Supabase Error (update_level): {e}")

        return AdaptiveRecommendation(**recommendation)

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing evaluation: {str(e)}",
        )



@router.get("/evaluation/history/{student_id}")
async def get_evaluation_history(student_id: int):
    """Mendapatkan riwayat evaluasi siswa."""
    records = get_progress(student_id)
    return {
        "student_id": student_id,
        "total_evaluations": len(records),
        "records": records,
    }
