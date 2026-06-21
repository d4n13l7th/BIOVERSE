"""
Bioverse - Adaptive Learning Engine
====================================
Endpoint utama (FastAPI) untuk menerima data evaluasi dari Laravel
dan merespons dengan rekomendasi penyesuaian tingkat kesulitan.
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Optional
from rules_logic import AdaptiveRulesEngine

app = FastAPI(
    title="Bioverse Adaptive Engine",
    description="Microservice sistem adaptif untuk platform pembelajaran ABK",
    version="1.0.0",
)

# Inisialisasi rules engine
rules_engine = AdaptiveRulesEngine()


# ─── Pydantic Schemas ────────────────────────────────────────────

class HistoryItem(BaseModel):
    """Satu entri riwayat belajar siswa."""
    module: str
    score: float
    response_time: float
    evaluated_at: Optional[str] = None


class EvaluationRequest(BaseModel):
    """Payload yang diterima dari Laravel."""
    student_id: int
    module: str
    score: float = Field(..., ge=0, le=100)
    response_time: float = Field(..., ge=0, description="Waktu respon dalam detik")
    history: list[HistoryItem] = []


class AdaptiveRecommendation(BaseModel):
    """Rekomendasi yang dikirim kembali ke Laravel."""
    action: str = Field(..., description="increase | decrease | maintain")
    new_level: Optional[int] = None
    audio_speed: float = 1.0
    animation_speed: float = 1.0
    message: str = ""
    fallback: bool = False


# ─── Endpoints ───────────────────────────────────────────────────

@app.get("/health")
async def health_check():
    """Health check endpoint untuk monitoring."""
    return {
        "status": "healthy",
        "engine": "adaptive_rules_v1",
        "version": "1.0.0",
    }


@app.post("/api/evaluate", response_model=AdaptiveRecommendation)
async def evaluate_student(request: EvaluationRequest):
    """
    Menerima data evaluasi siswa dari Laravel,
    menjalankan logika adaptif, dan mengembalikan rekomendasi.
    """
    try:
        recommendation = rules_engine.process(
            student_id=request.student_id,
            module=request.module,
            score=request.score,
            response_time=request.response_time,
            history=[h.model_dump() for h in request.history],
        )
        return AdaptiveRecommendation(**recommendation)

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing evaluation: {str(e)}",
        )


# ─── Entry Point ─────────────────────────────────────────────────

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
