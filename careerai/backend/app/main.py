from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import logging, time

from app.core.config import settings
from app.core.database import connect_db, disconnect_db
from app.api.routes import auth, resume, career, analytics, admin, chatbot

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("CareerAI starting...")
    await connect_db()
    yield
    await disconnect_db()

app = FastAPI(title="CareerAI API", version="1.0.0", docs_url="/api/docs", redoc_url="/api/redoc", lifespan=lifespan)

app.add_middleware(CORSMiddleware, allow_origins=settings.ALLOWED_ORIGINS, allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

@app.middleware("http")
async def timing(request: Request, call_next):
    s = time.time()
    r = await call_next(request)
    r.headers["X-Process-Time"] = str(round(time.time()-s, 4))
    return r

API = "/api/v1"
app.include_router(auth.router,      prefix=f"{API}/auth",      tags=["Auth"])
app.include_router(resume.router,    prefix=f"{API}/resume",    tags=["Resume"])
app.include_router(career.router,    prefix=f"{API}/careers",   tags=["Careers"])
app.include_router(analytics.router, prefix=f"{API}/analytics", tags=["Analytics"])
app.include_router(chatbot.router,   prefix=f"{API}/chatbot",   tags=["Chatbot"])
app.include_router(admin.router,     prefix=f"{API}/admin",     tags=["Admin"])

@app.get("/")
async def root(): return {"status":"ok","app":"CareerAI","version":"1.0.0"}

@app.get("/health")
async def health(): return {"status":"healthy"}

@app.exception_handler(Exception)
async def global_exc(request: Request, exc: Exception):
    logger.error(f"Unhandled: {exc}", exc_info=True)
    return JSONResponse(status_code=500, content={"detail":"Internal server error."})
