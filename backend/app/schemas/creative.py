# ============================================================
# backend/app/schemas/creative.py
# ============================================================

from pydantic import BaseModel, Field
from typing import List, Optional

class CreativeGenerateRequest(BaseModel):
    product_name: str = Field(..., description="Product or service name (e.g., 'CloudSync AI')")
    product_description: str = Field(..., description="What the product does and key value props")
    target_audience: str = Field("Tech-savvy professionals and business teams", description="Target buyer persona")
    tone: str = Field("Professional, persuasive, clear", description="Brand voice / tone")
    keywords: Optional[List[str]] = Field(default_factory=list, description="Keywords to incorporate into headlines")

class CreativeGenerateResponse(BaseModel):
    product_name: str
    headlines: List[str]      # 15 headlines, max 30 chars each
    descriptions: List[str]   # 4 descriptions, max 90 chars each
    call_to_actions: List[str]
    compliance_passed: bool
    suggestions: List[str]
