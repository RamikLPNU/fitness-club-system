from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse


from app.routers import (
    clients, trainers, memberships, classes,
    dates, visits, notifications, reports, stats
)

app = FastAPI(title="Fitness Club API")

# =========================
# CORS
# =========================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =========================
# API ROUTERS
# =========================
app.include_router(reports, prefix="/api/reports")
app.include_router(notifications, prefix="/api/notifications")
app.include_router(clients, prefix="/api/clients")
app.include_router(trainers, prefix="/api/trainers")
app.include_router(memberships, prefix="/api/memberships")
app.include_router(classes, prefix="/api/classes")
app.include_router(dates, prefix="/api/dates")
app.include_router(visits, prefix="/api/visits")
app.include_router(stats, prefix="/api/stats")


# =================================================
# 🔥 ФРОНТЕНД (ОЦЕ ГОЛОВНЕ ДЛЯ ВИКЛАДАЧА)
# =================================================

BASE_DIR = Path(__file__).resolve().parent.parent.parent
FRONTEND_DIR = BASE_DIR / "frontend"

app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")


@app.get("/")
def index():
    return FileResponse(FRONTEND_DIR / "index.html")


@app.get("/trainers")
def trainers_page():
    return FileResponse(FRONTEND_DIR / "trainers.html")


@app.get("/booking")
def booking_page():
    return FileResponse(FRONTEND_DIR / "booking.html")


@app.get("/admin_dashboard")
def admin_page():
    return FileResponse(FRONTEND_DIR / "admin/dashboard.html")


@app.get("/admin_reports")
def admin_reports_page():
    return FileResponse(FRONTEND_DIR / "admin/reports.html")


@app.get("/login")
def admin_page():
    return FileResponse(FRONTEND_DIR / "admin/login.html")
