"""
Bioverse - Main Application
==============================
Aplikasi FastAPI monolitik untuk platform pembelajaran
multisensori adaptif bagi Anak Berkebutuhan Khusus (ABK).

Arsitektur:
- FastAPI sebagai web server
- Jinja2 untuk HTML rendering
- Static files (CSS/JS/Audio/Animasi)
- REST API + Adaptive Engine

Jalankan:
    python main.py
    # atau
    uvicorn main:app --reload
"""

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from routers import pages, api, evaluation

# ─── FastAPI App ─────────────────────────────────────────────────

app = FastAPI(
    title="Bioverse — Adaptive Learning Platform",
    description=(
        "Platform pembelajaran multisensori adaptif untuk Anak Berkebutuhan Khusus (ABK). "
        "Mendukung 3 kategori: Autis, Tunanetra, dan Tunarungu dengan tata letak UI yang "
        "disesuaikan untuk setiap kategori."
    ),
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# ─── Static Files ───────────────────────────────────────────────

app.mount("/static", StaticFiles(directory="static"), name="static")

# ─── Routers ────────────────────────────────────────────────────

# HTML pages (Jinja2 templates)
app.include_router(pages.router)

# JSON API endpoints
app.include_router(api.router)

# Evaluation / Adaptive Engine
app.include_router(evaluation.router)


# ─── Health Check ───────────────────────────────────────────────

@app.get("/health", tags=["System"])
async def health_check():
    """Health check endpoint untuk monitoring."""
    return {
        "status": "healthy",
        "engine": "adaptive_rules_v1",
        "version": "2.0.0",
        "architecture": "FastAPI Monolith + Jinja2",
    }


# ─── Entry Point ────────────────────────────────────────────────

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
