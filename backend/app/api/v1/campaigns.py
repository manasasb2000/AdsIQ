# ============================================================
# backend/app/api/v1/campaigns.py
# ============================================================
#
# 📖 CAMPAIGN MANAGEMENT ROUTER
# Implements campaign creation, retrieval, updates, and deletion.
# ============================================================

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List

from app.core.database import get_db
from app.models.campaign import Campaign, Account, CampaignStatus
from app.schemas.campaign import CampaignCreate, CampaignResponse, CampaignUpdate

router = APIRouter()


@router.get("/", response_model=List[CampaignResponse])
async def list_campaigns(db: AsyncSession = Depends(get_db)):
    """List all Google Ads campaigns."""
    result = await db.execute(select(Campaign).order_by(Campaign.created_at.desc()))
    campaigns = result.scalars().all()
    return campaigns


@router.post("/", response_model=CampaignResponse, status_code=status.HTTP_201_CREATED)
async def create_campaign(
    campaign_in: CampaignCreate,
    db: AsyncSession = Depends(get_db)
):
    """
    Create a new Google Ads campaign.
    Automatically provisions a default Account if none exists.
    """
    # Check or create default demo account
    acc_result = await db.execute(select(Account).limit(1))
    account = acc_result.scalars().first()

    if not account:
        account = Account(
            customer_id="123-456-7890",
            name="Demo Google Ads Account",
            currency_code="INR",
            time_zone="Asia/Kolkata"
        )
        db.add(account)
        await db.flush()

    db_campaign = Campaign(
        account_id=account.id,
        name=campaign_in.name,
        campaign_type=campaign_in.campaign_type,
        bidding_strategy=campaign_in.bidding_strategy,
        daily_budget_micros=campaign_in.daily_budget_micros,
        campaign_goal=campaign_in.campaign_goal,
        target_locations=campaign_in.target_locations,
        target_languages=campaign_in.target_languages,
        status=CampaignStatus.PAUSED,
        ai_brief=campaign_in.ai_brief,
        resource_name=f"customers/{account.customer_id}/campaigns/simulated"
    )

    db.add(db_campaign)
    await db.commit()
    await db.refresh(db_campaign)

    return db_campaign


@router.get("/{campaign_id}", response_model=CampaignResponse)
async def get_campaign(campaign_id: str, db: AsyncSession = Depends(get_db)):
    """Get details of a single campaign by ID."""
    result = await db.execute(select(Campaign).where(Campaign.id == campaign_id))
    campaign = result.scalars().first()
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")
    return campaign
