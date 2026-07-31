# ============================================================
# backend/app/schemas/troubleshoot.py
# ============================================================

from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List

class TroubleshootRequest(BaseModel):
    error_code: Optional[str] = Field(None, description="Exact error code string, e.g. AUTHENTICATION_ERROR.OAUTH_TOKEN_EXPIRED")
    raw_log: Optional[str] = Field(None, description="Raw error output, stack trace, or JSON GoogleAdsFailure")
    programming_language: str = Field("python", description="Target programming language for code fix (python, javascript, java, php)")
    user_context: Optional[str] = Field(None, description="Additional background info on what you were trying to do")

class TroubleshootResponse(BaseModel):
    found: bool
    error_code: str
    category: str
    severity: str
    title: str
    description: str
    root_causes: List[str]
    diagnosis_steps: List[str]
    code_fix: str
    language: str
    prevention: List[str]
    docs_url: str
    ai_insights: Optional[str] = None
