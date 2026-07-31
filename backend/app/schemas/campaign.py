# ============================================================
# backend/app/schemas/campaign.py
# ============================================================
#
# 📖 WHAT IS THIS FILE?
# Contains Pydantic schemas for Google Ads campaign resources.
# Handles data validation for requests and formatting for responses.
# ============================================================

from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List, Dict, Any
from datetime import datetime
from app.models.campaign import CampaignStatus, CampaignType, BiddingStrategy, KeywordMatchType, AdType, AdGroupStatus


# ============================================================
# 📖 KEYWORD SCHEMAS
# ============================================================

class KeywordBase(BaseModel):
    text: str = Field(..., description="Keyword text (e.g. 'running shoes')")
    match_type: KeywordMatchType = Field(default=KeywordMatchType.EXACT, description="Match type: EXACT, PHRASE, or BROAD")
    bid_micros: Optional[int] = Field(default=15_000_000, description="CPC bid in micros (1 INR = 1,000,000 micros)")
    is_negative: bool = Field(default=False, description="Set True for negative keywords")

class KeywordCreate(KeywordBase):
    pass

class KeywordResponse(KeywordBase):
    id: str
    ad_group_id: str
    quality_score: Optional[int] = Field(default=None, description="Quality score between 1 and 10")
    status: str = "ENABLED"

    model_config = ConfigDict(from_attributes=True)


# ============================================================
# 📖 AD SCHEMAS
# ============================================================

class AdBase(BaseModel):
    ad_type: AdType = Field(default=AdType.RESPONSIVE_SEARCH_AD)
    headlines: List[str] = Field(..., description="List of headlines (up to 15, max 30 chars each)")
    descriptions: List[str] = Field(..., description="List of descriptions (up to 4, max 90 chars each)")
    final_urls: List[str] = Field(..., description="Destination URLs")
    display_url: Optional[str] = Field(default=None, description="Path shown in ad (e.g. example.com/shoes)")

class AdCreate(AdBase):
    ai_generated: bool = False
    generation_prompt: Optional[str] = None

class AdResponse(AdBase):
    id: str
    ad_group_id: str
    resource_name: Optional[str] = None
    policy_status: str = "ELIGIBLE"
    status: str = "ENABLED"
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


# ============================================================
# 📖 AD GROUP SCHEMAS
# ============================================================

class AdGroupBase(BaseModel):
    name: str = Field(..., description="Ad Group name (e.g. 'Men\'s Trail Running')")
    cpc_bid_micros: Optional[int] = Field(default=20_000_000)
    target_cpa_micros: Optional[int] = Field(default=None)
    target_roas: Optional[float] = Field(default=None)

class AdGroupCreate(AdGroupBase):
    keywords: Optional[List[KeywordCreate]] = Field(default=[], description="Initial keywords for this ad group")
    ads: Optional[List[AdCreate]] = Field(default=[], description="Initial ads for this ad group")

class AdGroupResponse(AdGroupBase):
    id: str
    campaign_id: str
    resource_name: Optional[str] = None
    status: AdGroupStatus = AdGroupStatus.ENABLED
    quality_score: Optional[int] = None
    keywords: List[KeywordResponse] = []
    ads: List[AdResponse] = []
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


# ============================================================
# 📖 CAMPAIGN SCHEMAS
# ============================================================

class CampaignBase(BaseModel):
    name: str = Field(..., min_length=3, max_length=255, description="Campaign name")
    campaign_type: CampaignType = Field(default=CampaignType.SEARCH)
    bidding_strategy: BiddingStrategy = Field(default=BiddingStrategy.MAXIMIZE_CLICKS)
    daily_budget_micros: int = Field(default=500_000_000, gt=0, description="Daily budget in micros (e.g. 500 INR = 500,000,000 micros)")
    campaign_goal: Optional[str] = Field(default="LEADS", description="Campaign goal (LEADS, SALES, WEBSITE_TRAFFIC)")
    target_locations: Optional[List[str]] = Field(default=["Hyderabad, Telangana, India"], description="Target cities/countries")
    target_languages: Optional[List[str]] = Field(default=["English"], description="Target languages")

class CampaignCreate(CampaignBase):
    ai_brief: Optional[str] = Field(default=None, description="Original natural language prompt used to generate this campaign")
    ad_groups: Optional[List[AdGroupCreate]] = Field(default=[], description="Optional initial ad groups")

class CampaignUpdate(BaseModel):
    name: Optional[str] = None
    status: Optional[CampaignStatus] = None
    daily_budget_micros: Optional[int] = None
    bidding_strategy: Optional[BiddingStrategy] = None

class CampaignResponse(CampaignBase):
    id: str
    account_id: str
    resource_name: Optional[str] = None
    status: CampaignStatus
    optimization_score: Optional[float] = Field(default=85.0, description="Optimization score percentage (0-100)")
    ad_groups: List[AdGroupResponse] = []
    ai_brief: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    # ConfigDict(from_attributes=True) allows Pydantic to automatically convert
    # SQLAlchemy ORM instances to Pydantic objects.
    model_config = ConfigDict(from_attributes=True)
