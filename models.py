"""
Bioverse - Pydantic Models
===========================
Skema data untuk validasi request/response.
Dimigrasi dari Laravel Eloquent Models (Student.php, ProgressTracker.php)
ke Pydantic v2 schemas.
"""

from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum


# ─── Enum Kategori ABK ──────────────────────────────────────────

class AbkCategory(str, Enum):
    """Kategori Anak Berkebutuhan Khusus yang didukung."""
    AUTIS = "autis"
    TUNANETRA = "tunanetra"
    TUNARUNGU = "tunarungu"


# ─── Student Schema ─────────────────────────────────────────────

class Student(BaseModel):
    """
    Representasi data siswa ABK.
    Dimigrasi dari App\\Models\\Student (Laravel).
    """
    id: int
    name: str
    abk_category: AbkCategory
    age: int = Field(..., ge=5, le=18)
    current_level: int = Field(default=1, ge=1, le=10)
    preferences: dict = Field(default_factory=dict)
    avatar_emoji: str = "👤"


# ─── Learning Module Schema ─────────────────────────────────────

class ContentStep(BaseModel):
    """Satu langkah dalam konten pembelajaran."""
    step: int
    title: str
    description: str
    subtitle: str = ""
    audio_file: Optional[str] = None
    animation_file: Optional[str] = None
    visual_cues: list[dict] = Field(default_factory=list)


class LearningModule(BaseModel):
    """Modul pembelajaran (Sistem Pencernaan)."""
    id: int
    title: str
    organ: str
    description: str
    icon: str = "🔬"
    content_steps: list[ContentStep] = Field(default_factory=list)


# ─── Quiz Schema ────────────────────────────────────────────────

class QuizOption(BaseModel):
    """Opsi jawaban kuis."""
    text: str
    icon: Optional[str] = None
    correct: bool = False


class QuizQuestion(BaseModel):
    """Satu pertanyaan kuis."""
    id: int
    module_id: int
    question: str
    options: list[QuizOption]
    explanation: str = ""


# ─── Progress Tracker Schema ────────────────────────────────────

class ProgressRecord(BaseModel):
    """
    Riwayat belajar siswa.
    Dimigrasi dari App\\Models\\ProgressTracker (Laravel).
    """
    student_id: int
    module_id: int
    module: str
    score: float = Field(..., ge=0, le=100)
    response_time: float = Field(..., ge=0, description="Waktu respon dalam detik")
    interactions: dict = Field(default_factory=dict)
    evaluated_at: Optional[str] = None


# ─── Evaluation Schemas ─────────────────────────────────────────

class HistoryItem(BaseModel):
    """Satu entri riwayat belajar siswa."""
    module: str
    score: float
    response_time: float
    evaluated_at: Optional[str] = None


class EvaluationRequest(BaseModel):
    """Payload evaluasi yang dikirim dari frontend."""
    student_id: int
    module: str
    score: float = Field(..., ge=0, le=100)
    response_time: float = Field(..., ge=0, description="Waktu respon dalam detik")
    history: list[HistoryItem] = []


class AdaptiveRecommendation(BaseModel):
    """Rekomendasi yang dikembalikan oleh adaptive engine."""
    action: str = Field(..., description="increase | decrease | maintain")
    new_level: Optional[int] = None
    audio_speed: float = 1.0
    animation_speed: float = 1.0
    message: str = ""
    fallback: bool = False
