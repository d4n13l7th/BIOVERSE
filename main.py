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

# Session router (Layer0)
from routers import session as session_router
app.include_router(session_router.router, prefix="/api/session", tags=["Layer0"])

# Optional routers for future layers (import if available)
try:
    from routers import jarvis as jarvis_router
    app.include_router(jarvis_router.router, prefix="/api/jarvis", tags=["Layer1"])
except Exception:
    pass
try:
    from routers import hook as hook_router
    app.include_router(hook_router.router, prefix="/api/hook", tags=["Layer2"])
except Exception:
    pass
try:
    from routers import visual as visual_router
    app.include_router(visual_router.router, prefix="/api/visual", tags=["Layer3"])
except Exception:
    pass


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
