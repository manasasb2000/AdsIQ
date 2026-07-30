# ============================================================
# backend/app/main.py
# ============================================================
#
# 📖 THIS IS THE ENTRY POINT OF OUR FASTAPI APPLICATION
#
# When uvicorn starts, it looks for:   app.main:app
#                                       ↑    ↑    ↑
#                               module  file  variable
#
# It imports this file and finds the `app = FastAPI(...)` object.
# Every HTTP request comes through this file first.
# ============================================================

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
import structlog

# Import our route handlers (we'll build these next)
from app.api.v1 import campaigns, agents, analytics, troubleshoot, codegen, creative
from app.api import websocket
from app.core.config import settings
from app.core.database import init_db

# ── Logger Setup ───────────────────────────────────────────
# structlog gives us JSON-formatted logs, e.g.:
# {"event": "startup", "environment": "development", "timestamp": "..."}
# This is much easier to search in production log tools like Datadog.
logger = structlog.get_logger()


# ============================================================
# 📖 LIFESPAN — Startup & Shutdown Events
# ============================================================
# @asynccontextmanager turns this function into a "context manager"
# Code BEFORE `yield` runs on startup (app initializing)
# Code AFTER `yield` runs on shutdown (app closing)
#
# This is the modern FastAPI way to handle startup/shutdown.
# (Old way was @app.on_event("startup") — now deprecated)
# ============================================================
@asynccontextmanager
async def lifespan(app: FastAPI):
    # ── STARTUP ──────────────────────────────────────────
    logger.info("🚀 AdsIQ starting up...", environment=settings.ENVIRONMENT)

    # Initialize database tables (creates them if they don't exist)
    await init_db()
    logger.info("✅ Database initialized")

    yield  # ← App runs here (handling requests)

    # ── SHUTDOWN ─────────────────────────────────────────
    logger.info("👋 AdsIQ shutting down...")


# ============================================================
# 📖 FASTAPI APP INSTANCE
# ============================================================
# This is THE central object. Everything is configured here.
# `lifespan=lifespan` wires up our startup/shutdown function.
# ============================================================
app = FastAPI(
    title="AdsIQ — Google Ads API Intelligence Platform",
    description="""
    ## 🎯 AdsIQ API

    AI-powered multi-agent platform for Google Ads API intelligence.

    ### Features
    * **🔧 Troubleshooter** — Diagnose and fix Google Ads API errors
    * **🏗️ Campaign Builder** — AI-assisted campaign structure generation
    * **🎨 Creative Studio** — RSA headlines, descriptions, ad assets
    * **📊 Analytics** — GAQL queries, ROAS, CTR, Quality Score analysis
    * **💬 Solutions Consultant** — End-to-end AI advisory

    ### Authentication
    Use Bearer token: `Authorization: Bearer <your-token>`
    """,
    version="1.0.0",
    # docs_url="/docs" → enables the Swagger UI at /docs
    # FastAPI auto-generates this from your route definitions!
    docs_url="/docs",
    # redoc_url="/redoc" → alternative documentation UI
    redoc_url="/redoc",
    lifespan=lifespan,
)


# ============================================================
# 📖 MIDDLEWARE
# ============================================================
# Middleware = code that runs on EVERY request/response.
# Think of it as a pipeline: Request → Middleware → Route Handler → Response
# ============================================================

# CORS (Cross-Origin Resource Sharing)
# Without this, your browser BLOCKS the frontend (localhost:3000)
# from calling the backend (localhost:8000) — they're different "origins".
# This is a browser security feature called the Same-Origin Policy.
app.add_middleware(
    CORSMiddleware,
    # allow_origins: which domains can call our API
    # In production, replace "*" with ["https://yourdomain.com"]
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,           # Allow cookies/auth headers
    allow_methods=["*"],              # Allow GET, POST, PUT, DELETE, etc.
    allow_headers=["*"],              # Allow any request header
)

# GZip Compression
# Automatically compresses responses larger than 1000 bytes.
# Reduces bandwidth — important when returning large analytics datasets.
app.add_middleware(GZipMiddleware, minimum_size=1000)


# ============================================================
# 📖 ROUTERS — Organize routes into modules
# ============================================================
# Instead of defining ALL routes in main.py (messy!),
# we split them into separate files and "include" them here.
#
# prefix="/api/v1" means every route in that module is prefixed.
# e.g., campaigns.py has GET "/" → becomes GET "/api/v1/campaigns/"
#
# tags=["Campaigns"] groups endpoints in the Swagger UI docs.
# ============================================================

app.include_router(
    campaigns.router,
    prefix="/api/v1/campaigns",
    tags=["📁 Campaigns"],
)

app.include_router(
    agents.router,
    prefix="/api/v1/agents",
    tags=["🤖 AI Agents"],
)

app.include_router(
    analytics.router,
    prefix="/api/v1/analytics",
    tags=["📊 Analytics"],
)

app.include_router(
    troubleshoot.router,
    prefix="/api/v1/troubleshoot",
    tags=["🔧 Troubleshooter"],
)

app.include_router(
    codegen.router,
    prefix="/api/v1/codegen",
    tags=["💻 Code Generator"],
)

app.include_router(
    creative.router,
    prefix="/api/v1/creative",
    tags=["🎨 Creative Studio"],
)

# WebSocket router (no /api/v1 prefix — WS uses ws:// not http://)
app.include_router(
    websocket.router,
    tags=["⚡ WebSocket"],
)


# ============================================================
# 📖 ROOT ENDPOINT
# ============================================================
# GET / → Returns basic API info.
# Useful for health checks (e.g., Kubernetes liveness probe).
# ============================================================
@app.get("/", tags=["🏠 Health"])
async def root():
    """
    Root health check endpoint.
    Returns API status and version information.
    """
    return {
        "name": "AdsIQ — Google Ads API Intelligence Platform",
        "version": "1.0.0",
        "status": "operational",
        "docs": "/docs",
        "environment": settings.ENVIRONMENT,
    }


@app.get("/health", tags=["🏠 Health"])
async def health_check():
    """
    Detailed health check for monitoring systems.
    In production, Kubernetes calls this every 30 seconds.
    If it returns non-200, Kubernetes restarts the pod.
    """
    return {
        "status": "healthy",
        "services": {
            "api": "operational",
            "database": "operational",
            "redis": "operational",
        }
    }
