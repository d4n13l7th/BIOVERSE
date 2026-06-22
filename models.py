"""
Bioverse - Pydantic Models
===========================
Skema data untuk validasi request/response.
Dimigrasi dari Laravel Eloquent Models (Student.php, ProgressTracker.php)
ke Pydantic v2 schemas.
"""

from pydantic import BaseModel, Field
from typing import Optional, Any, Dict, List
from enum import Enum
from datetime import datetime


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
    connecting_fact: Optional[str] = Field(default=None, description="Fakta penghubung untuk bridging Jarvis")
    vtt_url: Optional[str] = Field(default=None, description="URL subtitle VTT untuk Tunarungu")
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
    current_level: int = Field(default=1, ge=1, le=10, description="Level kesulitan siswa saat ini")
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


# ─── Phase 2 Session & Dependency Schemas ───────────────────────

class SessionState(BaseModel):
    """State real-time untuk tracking interaksi per sesi (Jarvis, Hook, Premack)."""
    session_id: str
    student_id: int
    current_topic: str
    is_idle: bool = False
    idle_duration: float = 0.0
    jarvis_mode: str = Field(default="active", description="active | silent | supportive")
    completed_topics: list[str] = Field(default_factory=list)


class TopicDependencyNode(BaseModel):
    """Graph dependencies untuk Reward Gate (Premack)."""
    topic_id: str
    title: str
    prerequisites: list[str] = Field(default_factory=list, description="List of topic_id required to unlock this topic")
    is_reward: bool = False
    reward_type: Optional[str] = None


# ─── Jarvis & Session Related Enums / Schemas (Phase 2) ─────────

class JarvisState(str, Enum):
    """Finite states untuk Jarvis VUI state machine."""
    IDLE_LISTENING = "IDLE_LISTENING"
    PROCESSING_QUERY = "PROCESSING_QUERY"
    TOPIC_VALID_IN_SCOPE = "TOPIC_VALID_IN_SCOPE"
    TOPIC_AHEAD_OF_LEVEL = "TOPIC_AHEAD_OF_LEVEL"
    TOPIC_UNKNOWN = "TOPIC_UNKNOWN"
    SPEAKING_RESPONSE = "SPEAKING_RESPONSE"


class JarvisQueryRequest(BaseModel):
    """Payload dari client ketika mengirim transcript ke Jarvis."""
    student_id: int
    session_id: str
    transcript: str


class JarvisQueryResponse(BaseModel):
    """Jawaban yang dikembalikan oleh endpoint Jarvis."""
    response_text: str
    action: Optional[str] = None
    fsm_state: JarvisState
    materi_content: Optional[Dict[str, Any]] = None


class HookIdleEvent(BaseModel):
    """Payload untuk event idle yang dikirim client ke Hook endpoint."""
    student_id: int
    session_id: str
    idle_duration: int
    current_screen: Optional[str] = None


class HookIdleResponse(BaseModel):
    """Respon dari server setelah memproses idle event."""
    escalation_level: int
    should_notify_caregiver: bool


class RewardGateStatus(BaseModel):
    """Status reward gate yang dibaca client."""
    student_id: int
    current_task_status: str
    reward_expires_at: Optional[datetime]
    interaction_budget_seconds: int


class RewardClaimRequest(BaseModel):
    """Payload untuk klaim reward."""
    student_id: int
    session_id: str


class VisualInteractionEvent(BaseModel):
    """Event yang berasal dari interaksi visual/haptic frontend."""
    student_id: int
    session_id: str
    element_id: str
    action_type: str
    is_correct: bool


class SessionStateCreate(BaseModel):
    """Payload minimal untuk membuat session_state baru."""
    student_id: int
    session_id: str


class SessionStateUpdate(BaseModel):
    """Partial update untuk session_state; semua field optional."""
    fsm_state: Optional[str] = None
    current_topic_id: Optional[int] = None
    last_query: Optional[str] = None
    last_topic_attempted: Optional[str] = None
    engagement_score: Optional[float] = None
    current_task_status: Optional[str] = None
    reward_expires_at: Optional[datetime] = None
    interaction_budget_seconds: Optional[int] = None
    hook_enabled: Optional[bool] = None
    hook_idle_threshold_seconds: Optional[int] = None
    last_interaction_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

