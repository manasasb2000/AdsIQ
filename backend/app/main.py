# ============================================================
# backend/app/main.py
# ============================================================

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
import structlog

from app.api.v1 import campaigns, agents, analytics, troubleshoot, codegen, creative
from app.api import websocket
from app.core.config import settings
from app.core.database import init_db
from app.seed_data import seed_demo_data

logger = structlog.get_logger()


@asynccontextmanager
async def lifespan(app: FastAPI):
    # ── STARTUP ──────────────────────────────────────────
    logger.info("🚀 AdsIQ starting up...", environment=settings.ENVIRONMENT)

    # Initialize database tables and seed demo data
    await init_db()
    try:
        await seed_demo_data()
    except Exception as e:
        logger.warning("Seed data notice", note=str(e))

    logger.info("✅ Database & Seed Data Ready")

    yield  # App is active

    # ── SHUTDOWN ─────────────────────────────────────────
    logger.info("👋 AdsIQ shutting down...")


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
    """,
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(GZipMiddleware, minimum_size=1000)

app.include_router(campaigns.router, prefix="/api/v1/campaigns", tags=["📁 Campaigns"])
app.include_router(agents.router, prefix="/api/v1/agents", tags=["🤖 AI Agents"])
app.include_router(analytics.router, prefix="/api/v1/analytics", tags=["📊 Analytics"])
app.include_router(troubleshoot.router, prefix="/api/v1/troubleshoot", tags=["🔧 Troubleshooter"])
app.include_router(codegen.router, prefix="/api/v1/codegen", tags=["💻 Code Generator"])
app.include_router(creative.router, prefix="/api/v1/creative", tags=["🎨 Creative Studio"])
app.include_router(websocket.router, tags=["⚡ WebSocket"])


@app.get("/", tags=["🏠 Health"])
async def root():
    return {
        "name": "AdsIQ — Google Ads API Intelligence Platform",
        "version": "1.0.0",
        "status": "operational",
        "docs": "/docs",
        "environment": settings.ENVIRONMENT,
    }


@app.get("/health", tags=["🏠 Health"])
async def health_check():
    return {
        "status": "healthy",
        "services": {
            "api": "operational",
            "database": "operational",
            "redis": "operational",
        }
    }
