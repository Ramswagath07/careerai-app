from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import logging
import os

from app.core.config import settings
from app.core.database import connect_db, disconnect_db
from app.api import auth, resume, careers, analytics, chatbot, admin, courses
from app.middleware.rate_limit import RateLimitMiddleware
from app.middleware.logging import LoggingMiddleware

logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(name)s | %(message)s")
logger = logging.getLogger(__name__)

app = FastAPI(
    title="CareerAI API",
    description="AI-powered Career Recommendation System with ATS Resume Scoring",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(LoggingMiddleware)
app.add_middleware(RateLimitMiddleware, max_requests=100, window_seconds=60)

os.makedirs("uploads", exist_ok=True)
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

@app.on_event("startup")
async def startup():
    logger.info("CareerAI API starting up...")
    await connect_db()
    logger.info("Database connected")

@app.on_event("shutdown")
async def shutdown():
    await disconnect_db()

app.include_router(auth.router,      prefix="/api/auth",      tags=["Authentication"])
app.include_router(resume.router,    prefix="/api/resume",    tags=["Resume"])
app.include_router(careers.router,   prefix="/api/careers",   tags=["Careers"])
app.include_router(analytics.router, prefix="/api/analytics", tags=["Analytics"])
app.include_router(chatbot.router,   prefix="/api/chatbot",   tags=["Chatbot"])
app.include_router(courses.router,   prefix="/api/courses",   tags=["Courses"])
app.include_router(admin.router,     prefix="/api/admin",     tags=["Admin"])

@app.get("/")
async def root():
    return {"status": "ok", "app": "CareerAI API", "version": "1.0.0"}

@app.get("/api/health")
async def health():
    return {"status": "healthy"}
