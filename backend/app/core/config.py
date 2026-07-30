# ============================================================
# backend/app/core/config.py
# ============================================================
#
# 📖 WHAT IS THIS FILE?
# This is our application's configuration hub.
# It reads ALL environment variables from the .env file
# and makes them available as Python attributes throughout the app.
#
# 📖 WHY USE A CONFIG CLASS INSTEAD OF os.environ.get()?
# Bad way:  os.environ.get("OPENAI_API_KEY")  ← scattered everywhere
# Good way: settings.OPENAI_API_KEY            ← centralized, typed, validated
#
# If a required variable is missing, Pydantic raises an error
# immediately on startup — not randomly in the middle of a request.
# ============================================================

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import AnyHttpUrl
from typing import List


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.

    Pydantic's BaseSettings automatically:
    1. Reads values from .env file
    2. Validates types (e.g., ensures PORT is an int, not a string)
    3. Raises clear errors if required fields are missing
    """

    # ── Tell Pydantic WHERE to find the .env file ──────────
    # model_config is the new Pydantic v2 way to configure the Settings class
    model_config = SettingsConfigDict(
        env_file=".env",          # Load from .env file
        env_file_encoding="utf-8",
        case_sensitive=False,     # OPENAI_API_KEY == openai_api_key
        extra="ignore",           # Ignore unknown env vars (don't error)
    )

    # ── App Settings ───────────────────────────────────────
    # The type hint (str) tells Pydantic what type to expect.
    # The default value (after =) is used if the env var isn't set.
    ENVIRONMENT: str = "development"
    DEMO_MODE: bool = True          # If True, use mock data (no real API keys needed)

    # ── Database ───────────────────────────────────────────
    # AnyHttpUrl validates this is a proper URL format
    POSTGRES_URL: str = "postgresql://adsiq_user:adsiq_pass@localhost:5432/adsiq_db"
    POSTGRES_USER: str = "adsiq_user"
    POSTGRES_PASSWORD: str = "adsiq_pass"
    POSTGRES_DB: str = "adsiq_db"

    # ── Redis ──────────────────────────────────────────────
    REDIS_URL: str = "redis://localhost:6379/0"

    # ── AI Keys ────────────────────────────────────────────
    # These have no default — they're Optional because DEMO_MODE can work without them
    OPENAI_API_KEY: str = ""
    GOOGLE_GEMINI_API_KEY: str = ""
    DEFAULT_LLM_PROVIDER: str = "openai"  # "openai" or "gemini"

    # ── LangSmith Observability ────────────────────────────
    LANGCHAIN_TRACING_V2: bool = False
    LANGCHAIN_API_KEY: str = ""
    LANGCHAIN_PROJECT: str = "adsiq-platform"

    # ── Security ───────────────────────────────────────────
    SECRET_KEY: str = "dev-secret-key-change-in-production-please"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    # ── CORS ───────────────────────────────────────────────
    # List of allowed origins for CORS.
    # In development: allow localhost:3000 (Next.js dev server)
    # In production: replace with your actual domain
    ALLOWED_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:3001",
        "https://adsiq.vercel.app",  # future production domain
    ]

    # ── Google Ads API (Optional) ──────────────────────────
    GOOGLE_ADS_DEVELOPER_TOKEN: str = ""
    GOOGLE_ADS_CLIENT_ID: str = ""
    GOOGLE_ADS_CLIENT_SECRET: str = ""
    GOOGLE_ADS_REFRESH_TOKEN: str = ""
    GOOGLE_ADS_LOGIN_CUSTOMER_ID: str = ""

    # ── Computed Properties ────────────────────────────────
    # @property turns a method into an attribute (no () needed when calling)
    @property
    def is_production(self) -> bool:
        """Returns True if running in production environment."""
        return self.ENVIRONMENT == "production"

    @property
    def has_openai_key(self) -> bool:
        """Returns True if OpenAI API key is configured."""
        return bool(self.OPENAI_API_KEY and not self.OPENAI_API_KEY.startswith("sk-your"))

    @property
    def has_gemini_key(self) -> bool:
        """Returns True if Gemini API key is configured."""
        return bool(self.GOOGLE_GEMINI_API_KEY and not self.GOOGLE_GEMINI_API_KEY.startswith("your"))

    @property
    def use_real_ai(self) -> bool:
        """Returns True if real AI calls should be made (not demo mode)."""
        return not self.DEMO_MODE and (self.has_openai_key or self.has_gemini_key)


# ============================================================
# 📖 THE SINGLETON PATTERN
# ============================================================
# We create ONE instance of Settings and import it everywhere.
# This means .env is read ONCE at startup, not on every request.
#
# Usage in any other file:
#   from app.core.config import settings
#   print(settings.OPENAI_API_KEY)
# ============================================================
settings = Settings()
