# ============================================================
# backend/app/models/campaign.py
# ============================================================
#
# 📖 WHAT ARE MODELS?
# A model is a Python class that maps to a database TABLE.
# Instead of writing raw SQL, you work with Python objects.
#
# SQLAlchemy ORM example:
#   campaign = Campaign(name="Shoe Sale", budget=50000)
#   db.add(campaign)                # INSERT INTO campaigns ...
#   await db.commit()
#   print(campaign.id)              # Get the auto-generated ID
#
# 📖 WHY DOES THIS STRUCTURE MATTER FOR THE GOOGLE PSE ROLE?
# The Google Ads API has a strict hierarchy:
#   Manager Account (MCC)
#     └── Customer Account
#           └── Campaign
#                 └── Ad Group
#                       ├── Keyword (Criterion)
#                       └── Ad (AdGroupAd)
#
# Our models mirror this EXACTLY — showing interviewers you
# deeply understand how the Google Ads API is structured.
# ============================================================

import uuid
from datetime import datetime
from typing import Optional, List
from sqlalchemy import (
    String, Integer, Float, Boolean, DateTime, ForeignKey,
    Enum as SAEnum, Text, JSON, BigInteger
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
import enum

from app.core.database import Base


# ============================================================
# 📖 PYTHON ENUMS for Google Ads API constants
# ============================================================
# Using Enum instead of raw strings prevents typos like
# "ACTVE" instead of "ACTIVE" — Python raises an error immediately.
# These mirror the exact enum names in the Google Ads API.
# ============================================================

class CampaignStatus(str, enum.Enum):
    """Mirrors CampaignStatus enum in Google Ads API."""
    ENABLED = "ENABLED"
    PAUSED = "PAUSED"
    REMOVED = "REMOVED"


class CampaignType(str, enum.Enum):
    """
    Mirrors AdvertisingChannelType in Google Ads API.
    Determines where ads appear.
    """
    SEARCH = "SEARCH"           # Text ads on Google Search results
    DISPLAY = "DISPLAY"         # Image ads across the Google Display Network
    SHOPPING = "SHOPPING"       # Product listing ads
    VIDEO = "VIDEO"             # YouTube video ads
    PERFORMANCE_MAX = "PERFORMANCE_MAX"  # Google's AI-driven all-channel campaign


class BiddingStrategy(str, enum.Enum):
    """
    Mirrors BiddingStrategyType in Google Ads API.
    Determines HOW you bid in auctions.

    📖 INTERVIEW KNOWLEDGE:
    - MANUAL_CPC: You set each bid manually. Full control, high effort.
    - TARGET_CPA: AI bids to get conversions at your target cost-per-action.
    - TARGET_ROAS: AI bids to maximize revenue at your target return-on-ad-spend.
    - MAXIMIZE_CONVERSIONS: AI maximizes total conversions within your budget.
    - MAXIMIZE_CONVERSION_VALUE: AI maximizes total conversion value.
    """
    MANUAL_CPC = "MANUAL_CPC"
    TARGET_CPA = "TARGET_CPA"
    TARGET_ROAS = "TARGET_ROAS"
    MAXIMIZE_CONVERSIONS = "MAXIMIZE_CONVERSIONS"
    MAXIMIZE_CONVERSION_VALUE = "MAXIMIZE_CONVERSION_VALUE"
    MAXIMIZE_CLICKS = "MAXIMIZE_CLICKS"
    TARGET_IMPRESSION_SHARE = "TARGET_IMPRESSION_SHARE"


class AdGroupStatus(str, enum.Enum):
    ENABLED = "ENABLED"
    PAUSED = "PAUSED"
    REMOVED = "REMOVED"


class KeywordMatchType(str, enum.Enum):
    """
    📖 INTERVIEW KNOWLEDGE — Keyword Match Types:
    - EXACT: [running shoes] → only matches "running shoes"
    - PHRASE: "running shoes" → matches "buy running shoes" but not "shoes for running"
    - BROAD: running shoes → matches "jogging sneakers", synonyms, related searches
    """
    EXACT = "EXACT"
    PHRASE = "PHRASE"
    BROAD = "BROAD"


class AdType(str, enum.Enum):
    """Types of ads in the Google Ads API."""
    RESPONSIVE_SEARCH_AD = "RESPONSIVE_SEARCH_AD"   # RSA: up to 15 headlines, 4 descriptions
    EXPANDED_TEXT_AD = "EXPANDED_TEXT_AD"            # Legacy format (deprecated)
    RESPONSIVE_DISPLAY_AD = "RESPONSIVE_DISPLAY_AD"  # Display network
    CALL_AD = "CALL_AD"                              # Phone call focused


# ============================================================
# 📖 TABLE: accounts
# ============================================================
# Represents a Google Ads Customer Account.
# In the real API: customers/{customer_id}
# ============================================================
class Account(Base):
    __tablename__ = "accounts"

    # UUID primary key — more secure than sequential integers
    # (can't guess other users' IDs by incrementing)
    id: Mapped[str] = mapped_column(
        UUID(as_uuid=False), primary_key=True, default=lambda: str(uuid.uuid4())
    )

    # customer_id mirrors Google Ads API's customer ID (e.g., "123-456-7890")
    customer_id: Mapped[str] = mapped_column(String(20), unique=True, index=True)
    name: Mapped[str] = mapped_column(String(255))
    currency_code: Mapped[str] = mapped_column(String(3), default="INR")  # ISO 4217
    time_zone: Mapped[str] = mapped_column(String(50), default="Asia/Kolkata")
    is_demo: Mapped[bool] = mapped_column(Boolean, default=True)

    # SQLAlchemy timestamps
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationship: one account → many campaigns
    # back_populates="account" creates the reverse: campaign.account
    campaigns: Mapped[List["Campaign"]] = relationship("Campaign", back_populates="account")


# ============================================================
# 📖 TABLE: campaigns
# ============================================================
# Core entity. Each campaign has a type, budget, bidding strategy.
# In the real API: customers/{customer_id}/campaigns/{campaign_id}
# ============================================================
class Campaign(Base):
    __tablename__ = "campaigns"

    id: Mapped[str] = mapped_column(UUID(as_uuid=False), primary_key=True, default=lambda: str(uuid.uuid4()))
    account_id: Mapped[str] = mapped_column(UUID(as_uuid=False), ForeignKey("accounts.id"), index=True)

    # Google Ads API campaign resource name format:
    # "customers/1234567890/campaigns/9876543210"
    resource_name: Mapped[Optional[str]] = mapped_column(String(255))
    name: Mapped[str] = mapped_column(String(255))
    status: Mapped[CampaignStatus] = mapped_column(SAEnum(CampaignStatus), default=CampaignStatus.PAUSED)
    campaign_type: Mapped[CampaignType] = mapped_column(SAEnum(CampaignType), default=CampaignType.SEARCH)
    bidding_strategy: Mapped[BiddingStrategy] = mapped_column(SAEnum(BiddingStrategy), default=BiddingStrategy.MAXIMIZE_CLICKS)

    # Budget in MICROS (Google Ads API stores money as integers × 1,000,000)
    # 📖 WHY MICROS? Avoids floating-point precision errors in money calculations.
    # 50000 INR = 50,000,000,000 micros
    daily_budget_micros: Mapped[int] = mapped_column(BigInteger, default=1000000)  # 1 INR default

    # Campaign goal (awareness, leads, sales, etc.)
    campaign_goal: Mapped[Optional[str]] = mapped_column(String(100))

    # Target locations as JSON array (e.g., ["Hyderabad", "Mumbai"])
    target_locations: Mapped[Optional[dict]] = mapped_column(JSON)

    # Target languages as JSON array (e.g., ["English", "Telugu"])
    target_languages: Mapped[Optional[dict]] = mapped_column(JSON)

    start_date: Mapped[Optional[datetime]] = mapped_column(DateTime)
    end_date: Mapped[Optional[datetime]] = mapped_column(DateTime)

    # AI-generated fields
    ai_brief: Mapped[Optional[str]] = mapped_column(Text)  # Original brief from user
    optimization_score: Mapped[Optional[float]] = mapped_column(Float)  # 0-100

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    account: Mapped["Account"] = relationship("Account", back_populates="campaigns")
    ad_groups: Mapped[List["AdGroup"]] = relationship("AdGroup", back_populates="campaign")
    metrics: Mapped[List["PerformanceMetric"]] = relationship("PerformanceMetric", back_populates="campaign")


# ============================================================
# 📖 TABLE: ad_groups
# ============================================================
# Ad groups organize ads and keywords within a campaign.
# Best practice: keep each ad group tightly themed (10-20 keywords).
# ============================================================
class AdGroup(Base):
    __tablename__ = "ad_groups"

    id: Mapped[str] = mapped_column(UUID(as_uuid=False), primary_key=True, default=lambda: str(uuid.uuid4()))
    campaign_id: Mapped[str] = mapped_column(UUID(as_uuid=False), ForeignKey("campaigns.id"), index=True)
    resource_name: Mapped[Optional[str]] = mapped_column(String(255))
    name: Mapped[str] = mapped_column(String(255))
    status: Mapped[AdGroupStatus] = mapped_column(SAEnum(AdGroupStatus), default=AdGroupStatus.ENABLED)

    # Default CPC bid for keywords in this group (in micros)
    cpc_bid_micros: Mapped[Optional[int]] = mapped_column(BigInteger)
    target_cpa_micros: Mapped[Optional[int]] = mapped_column(BigInteger)
    target_roas: Mapped[Optional[float]] = mapped_column(Float)

    # Quality Score: 1-10. Key Google Ads metric.
    # Higher QS = lower CPC + better ad position.
    quality_score: Mapped[Optional[int]] = mapped_column(Integer)

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    campaign: Mapped["Campaign"] = relationship("Campaign", back_populates="ad_groups")
    keywords: Mapped[List["Keyword"]] = relationship("Keyword", back_populates="ad_group")
    ads: Mapped[List["Ad"]] = relationship("Ad", back_populates="ad_group")


# ============================================================
# 📖 TABLE: keywords
# ============================================================
# Keywords trigger your ads when users search for them.
# In the API: customers/{cid}/adGroupCriteria/{cid}~{criterion_id}
# ============================================================
class Keyword(Base):
    __tablename__ = "keywords"

    id: Mapped[str] = mapped_column(UUID(as_uuid=False), primary_key=True, default=lambda: str(uuid.uuid4()))
    ad_group_id: Mapped[str] = mapped_column(UUID(as_uuid=False), ForeignKey("ad_groups.id"), index=True)
    text: Mapped[str] = mapped_column(String(255))
    match_type: Mapped[KeywordMatchType] = mapped_column(SAEnum(KeywordMatchType))
    bid_micros: Mapped[Optional[int]] = mapped_column(BigInteger)
    quality_score: Mapped[Optional[int]] = mapped_column(Integer)  # 1-10
    status: Mapped[str] = mapped_column(String(20), default="ENABLED")
    is_negative: Mapped[bool] = mapped_column(Boolean, default=False)  # Negative keywords exclude traffic

    ad_group: Mapped["AdGroup"] = relationship("AdGroup", back_populates="keywords")


# ============================================================
# 📖 TABLE: ads
# ============================================================
# The actual ad creative shown to users.
# RSA (Responsive Search Ads) is the primary format today.
# ============================================================
class Ad(Base):
    __tablename__ = "ads"

    id: Mapped[str] = mapped_column(UUID(as_uuid=False), primary_key=True, default=lambda: str(uuid.uuid4()))
    ad_group_id: Mapped[str] = mapped_column(UUID(as_uuid=False), ForeignKey("ad_groups.id"), index=True)
    resource_name: Mapped[Optional[str]] = mapped_column(String(255))
    ad_type: Mapped[AdType] = mapped_column(SAEnum(AdType), default=AdType.RESPONSIVE_SEARCH_AD)

    # RSA fields — stored as JSON arrays
    # Max: 15 headlines (30 chars each), 4 descriptions (90 chars each)
    headlines: Mapped[Optional[dict]] = mapped_column(JSON)       # ["Headline 1", "Headline 2", ...]
    descriptions: Mapped[Optional[dict]] = mapped_column(JSON)    # ["Description 1", ...]
    final_urls: Mapped[Optional[dict]] = mapped_column(JSON)      # ["https://example.com/page"]

    # Display URL (shown in the ad): example.com/path
    display_url: Mapped[Optional[str]] = mapped_column(String(255))

    # Policy status (Google reviews all ads for policy compliance)
    policy_status: Mapped[str] = mapped_column(String(50), default="ELIGIBLE")
    status: Mapped[str] = mapped_column(String(20), default="ENABLED")

    # AI generation metadata
    ai_generated: Mapped[bool] = mapped_column(Boolean, default=False)
    generation_prompt: Mapped[Optional[str]] = mapped_column(Text)

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    ad_group: Mapped["AdGroup"] = relationship("AdGroup", back_populates="ads")


# ============================================================
# 📖 TABLE: performance_metrics
# ============================================================
# Time-series performance data for campaigns.
# Mirrors the Google Ads API reporting service (GAQL queries).
# ============================================================
class PerformanceMetric(Base):
    __tablename__ = "performance_metrics"

    id: Mapped[str] = mapped_column(UUID(as_uuid=False), primary_key=True, default=lambda: str(uuid.uuid4()))
    campaign_id: Mapped[str] = mapped_column(UUID(as_uuid=False), ForeignKey("campaigns.id"), index=True)
    date: Mapped[datetime] = mapped_column(DateTime, index=True)

    # 📖 Core Google Ads metrics (what PSEs analyze every day):
    impressions: Mapped[int] = mapped_column(Integer, default=0)   # How many times ad was shown
    clicks: Mapped[int] = mapped_column(Integer, default=0)         # How many times ad was clicked
    cost_micros: Mapped[int] = mapped_column(BigInteger, default=0) # Total spend (in micros)
    conversions: Mapped[float] = mapped_column(Float, default=0.0)  # Desired actions completed
    conversion_value: Mapped[float] = mapped_column(Float, default=0.0)  # Revenue from conversions

    # Derived metrics (computed from the above):
    # ctr = clicks / impressions
    # avg_cpc = cost / clicks
    # roas = conversion_value / cost
    # These are stored for fast querying (no calculation at read time)
    ctr: Mapped[Optional[float]] = mapped_column(Float)              # Click-through rate
    average_cpc_micros: Mapped[Optional[int]] = mapped_column(BigInteger)  # Avg cost per click
    roas: Mapped[Optional[float]] = mapped_column(Float)             # Return on ad spend
    impression_share: Mapped[Optional[float]] = mapped_column(Float) # % of auctions we appeared in

    campaign: Mapped["Campaign"] = relationship("Campaign", back_populates="metrics")
