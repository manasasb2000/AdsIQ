# ============================================================
# backend/app/api/v1/troubleshoot.py
# ============================================================

from fastapi import APIRouter, HTTPException
from typing import List, Dict, Any

from app.schemas.troubleshoot import TroubleshootRequest, TroubleshootResponse
from app.ads_api_sim.error_library import get_error_by_code, GOOGLE_ADS_ERROR_LIBRARY
from app.agents.graph import AdsIQAgentEngine

router = APIRouter()


@router.post("/", response_model=TroubleshootResponse)
async def troubleshoot_error(request: TroubleshootRequest):
    """
    Diagnose a Google Ads API error using the AI Troubleshooter.
    Parses error code, extracts root cause, and generates fixed code.
    """
    code_to_search = request.error_code

    if not code_to_search and request.raw_log:
        for code in GOOGLE_ADS_ERROR_LIBRARY.keys():
            if code in request.raw_log:
                code_to_search = code
                break

    if not code_to_search:
        code_to_search = "AUTHENTICATION_ERROR.OAUTH_TOKEN_EXPIRED"

    error_info = get_error_by_code(code_to_search)

    fixes = error_info.get("fixes", {})
    code_fix = fixes.get(request.programming_language.lower(), fixes.get("python", "# Code fix available in Python"))

    return TroubleshootResponse(
        found=error_info.get("found", True),
        error_code=code_to_search,
        category=error_info.get("category", "API Error"),
        severity=error_info.get("severity", "high"),
        title=error_info.get("title", "Google Ads API Error"),
        description=error_info.get("description", ""),
        root_causes=error_info.get("root_causes", []),
        diagnosis_steps=error_info.get("diagnosis_steps", []),
        code_fix=code_fix,
        language=request.programming_language,
        prevention=error_info.get("prevention", []),
        docs_url=error_info.get("docs_url", "https://developers.google.com/google-ads/api/docs"),
        ai_insights=f"Google PSE Recommendation: Ensure you log the request_id from GoogleAdsFailure. Check OAuth scopes and refresh tokens."
    )


@router.get("/library")
async def get_error_library():
    """Browse the complete Google Ads API error knowledge base."""
    return {
        "total_errors": len(GOOGLE_ADS_ERROR_LIBRARY),
        "errors": [
            {
                "code": code,
                "title": details.get("title"),
                "category": details.get("category"),
                "severity": details.get("severity")
            }
            for code, details in GOOGLE_ADS_ERROR_LIBRARY.items()
        ]
    }
