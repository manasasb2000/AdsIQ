# ============================================================
# backend/app/core/database.py
# ============================================================
#
# 📖 WHAT IS THIS FILE?
# This sets up the connection between FastAPI and PostgreSQL.
# It uses SQLAlchemy's ASYNC engine — meaning database queries
# don't block the server. While waiting for a DB response,
# FastAPI can handle other incoming requests simultaneously.
#
# 📖 THE CONNECTION POOL
# We don't open/close a DB connection on every request (slow!).
# Instead, SQLAlchemy maintains a "pool" of reusable connections.
# Like a taxi stand — taxis wait ready, passengers (requests)
# grab one, use it, and return it to the pool.
# ============================================================

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import text
import structlog

from app.core.config import settings

logger = structlog.get_logger()


# ============================================================
# 📖 ASYNC DATABASE ENGINE
# ============================================================
# The engine is the core database connection.
# "postgresql+asyncpg://" means: use PostgreSQL via the asyncpg driver.
# We replace "postgresql://" with "postgresql+asyncpg://" for async support.
# ============================================================
DATABASE_URL = settings.POSTGRES_URL.replace(
    "postgresql://", "postgresql+asyncpg://"
)

engine = create_async_engine(
    DATABASE_URL,
    # echo=True logs every SQL query to the console.
    # Useful for debugging in development, disable in production.
    echo=settings.ENVIRONMENT == "development",
    # Pool settings — how many DB connections to maintain:
    pool_size=10,          # Keep 10 connections open
    max_overflow=20,       # Allow 20 more when all 10 are busy
    pool_pre_ping=True,    # Test connections before using (detect dead ones)
)


# ============================================================
# 📖 SESSION FACTORY
# ============================================================
# A "session" represents ONE unit of work with the database.
# Think of it like a shopping cart: you add items (queries),
# then checkout (commit) or abandon (rollback).
#
# async_sessionmaker creates new sessions on demand.
# expire_on_commit=False → objects remain usable after commit.
# ============================================================
AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


# ============================================================
# 📖 BASE CLASS FOR ALL MODELS
# ============================================================
# All our database table classes inherit from this Base.
# SQLAlchemy uses it to discover which classes → which tables.
# ============================================================
class Base(DeclarativeBase):
    pass


# ============================================================
# 📖 DEPENDENCY INJECTION — get_db()
# ============================================================
# FastAPI's dependency injection system is one of its superpowers.
# Instead of creating a DB session in every route handler,
# we define it ONCE here and FastAPI injects it automatically.
#
# Usage in a route:
#   async def get_campaigns(db: AsyncSession = Depends(get_db)):
#       campaigns = await db.execute(select(Campaign))
#
# The `yield` makes this a "generator function":
# - Code before yield: runs BEFORE the route handler (open session)
# - Code after yield: runs AFTER the route handler (close session)
# This guarantees the session always closes, even if an error occurs.
# ============================================================
async def get_db():
    """
    Dependency that provides a database session per request.
    Automatically commits on success, rolls back on error.
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session           # Give the session to the route handler
            await session.commit()  # Success → save changes to DB
        except Exception:
            await session.rollback()  # Error → undo all changes
            raise                     # Re-raise the exception (so FastAPI returns error)


# ============================================================
# 📖 DATABASE INITIALIZATION
# ============================================================
# Called once on app startup (from main.py lifespan).
# Creates all tables defined in our models IF they don't exist yet.
# "create_all" is safe to call repeatedly — it skips existing tables.
# ============================================================
async def init_db():
    """
    Create all database tables on startup.
    Imports all models so SQLAlchemy knows about them.
    """
    # Import all models here so Base knows about them before create_all.
    # This is a common pattern — the import registers the model with Base.
    from app.models import campaign, agent_run, metric  # noqa: F401

    async with engine.begin() as conn:
        # create_all: creates any tables that don't exist yet
        # checkfirst=True: skip tables that already exist (idempotent)
        await conn.run_sync(Base.metadata.create_all)

    logger.info("✅ All database tables created/verified")


async def check_db_connection() -> bool:
    """Test if database is reachable. Used in health checks."""
    try:
        async with AsyncSessionLocal() as session:
            await session.execute(text("SELECT 1"))
        return True
    except Exception as e:
        logger.error("❌ Database connection failed", error=str(e))
        return False
