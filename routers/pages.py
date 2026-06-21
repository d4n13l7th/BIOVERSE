"""
Bioverse - Page Routes (Jinja2 HTML)
=====================================
Rute-rute halaman yang merender template HTML.
Menggunakan query real-time Supabase Python Client.
"""

from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from supabase import create_client, Client
import os

# Tetap pertahankan import get_students untuk halaman index
from database import get_students

router = APIRouter(tags=["Pages"])
templates = Jinja2Templates(directory="templates")

# Inisialisasi Supabase Client dari Environment Variable
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# Menggunakan instance supabase yang global (bisa null jika kredensial belum ada)
# Untuk menghindari error crash saat start tanpa .env, kita cek ketersediaan URL dan KEY
if SUPABASE_URL and SUPABASE_KEY:
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
else:
    supabase = None

async def get_materi_by_category(kategori: str, level: int = 1):
    if not supabase:
        return None
    try:
        response = supabase.table("materi").select("*").eq("kategori", kategori).eq("level", level).execute()
        return response.data[0] if response.data else None
    except Exception as e:
        print(f"Error fetch materi: {e}")
        return None

async def get_kuis_by_materi_id(materi_id: int):
    if not supabase:
        return []
    try:
        response = supabase.table("kuis").select("*").eq("materi_id", materi_id).execute()
        return response.data if response.data else []
    except Exception as e:
        print(f"Error fetch kuis: {e}")
        return []

@router.get("/", name="home")
async def index(request: Request):
    """
    Halaman utama — Netflix-style profile selector.
    Menampilkan kartu profil semua siswa untuk dipilih.
    """
    students = get_students()
    return templates.TemplateResponse("index.html", {
        "request": request,
        "students": students,
        "page_title": "BIOVERSE — Pilih Kategori ABK",
    })

@router.get("/learn/autis", response_class=HTMLResponse)
async def route_learn_autis(request: Request):
    data = await get_materi_by_category("autis", level=1)
    kuis_data = await get_kuis_by_materi_id(data["id"]) if data else []
    return templates.TemplateResponse("learn_autis.html", {
        "request": request,
        "page_title": "BIOVERSE - Ruang Belajar Autis",
        "materi": data,
        "quiz_questions": kuis_data
    })

@router.get("/learn/tunanetra", response_class=HTMLResponse)
async def route_learn_tunanetra(request: Request):
    data = await get_materi_by_category("tunanetra", level=1)
    kuis_data = await get_kuis_by_materi_id(data["id"]) if data else []
    return templates.TemplateResponse("learn_tunanetra.html", {
        "request": request,
        "page_title": "BIOVERSE - Ruang Belajar Tunanetra",
        "materi": data,
        "quiz_questions": kuis_data
    })

@router.get("/learn/tunarungu", response_class=HTMLResponse)
async def route_learn_tunarungu(request: Request):
    data = await get_materi_by_category("tunarungu", level=1)
    kuis_data = await get_kuis_by_materi_id(data["id"]) if data else []
    return templates.TemplateResponse("learn_tunarungu.html", {
        "request": request,
        "page_title": "BIOVERSE - Ruang Belajar Tunarungu",
        "materi": data,
        "quiz_questions": kuis_data
    })
