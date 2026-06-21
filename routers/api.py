"""
Bioverse - API Routes (JSON)
==============================
Endpoint REST API untuk data siswa, modul, dan progress.
Menggantikan routes/api.php (Laravel).
Semua endpoint otomatis terdokumentasi di Swagger UI (/docs).
"""

from fastapi import APIRouter, HTTPException

from database import (
    get_students, get_student, get_modules, get_module,
    get_quiz_questions, get_progress,
)
from models import Student, LearningModule, QuizQuestion, ProgressRecord

router = APIRouter(prefix="/api", tags=["API"])


# ─── Students ───────────────────────────────────────────────────

@router.get("/students", response_model=list[Student])
async def list_students():
    """Mendapatkan daftar semua siswa."""
    return get_students()


@router.get("/students/{student_id}", response_model=Student)
async def get_student_detail(student_id: int):
    """Mendapatkan detail siswa berdasarkan ID."""
    student = get_student(student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Siswa tidak ditemukan")
    return student


# ─── Modules ────────────────────────────────────────────────────

@router.get("/modules", response_model=list[LearningModule])
async def list_modules():
    """Mendapatkan daftar semua modul pembelajaran."""
    return get_modules()


@router.get("/modules/{module_id}", response_model=LearningModule)
async def get_module_detail(module_id: int):
    """Mendapatkan detail modul berdasarkan ID."""
    module = get_module(module_id)
    if not module:
        raise HTTPException(status_code=404, detail="Modul tidak ditemukan")
    return module


# ─── Quiz ───────────────────────────────────────────────────────

@router.get("/quiz/{module_id}", response_model=list[QuizQuestion])
async def get_quiz(module_id: int):
    """Mendapatkan pertanyaan kuis untuk modul tertentu."""
    questions = get_quiz_questions(module_id)
    if not questions:
        raise HTTPException(status_code=404, detail="Kuis tidak ditemukan untuk modul ini")
    return questions


# ─── Progress ───────────────────────────────────────────────────

@router.get("/progress/{student_id}", response_model=list[ProgressRecord])
async def get_student_progress(student_id: int):
    """Mendapatkan riwayat progress belajar siswa."""
    student = get_student(student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Siswa tidak ditemukan")
    return get_progress(student_id)
