# ============================================================
# backend/app/seed_data.py
# ============================================================
#
# 📖 DEMO DATA SEEDING SCRIPT
# Populates PostgreSQL with realistic Google Ads campaigns,
# ad groups, keywords, ads, performance metrics, and error logs.
# ============================================================

import asyncio
from datetime import datetime, timedelta
import random
from sqlalchemy import select
import structlog

from app.core.database import AsyncSessionLocal, engine, init_db
from app.models.campaign import Account, Campaign, AdGroup, Keyword, Ad, PerformanceMetric, CampaignStatus, CampaignType, BiddingStrategy, KeywordMatchType, AdType, AdGroupStatus
from app.models.agent_run import AgentRun, AgentLog, AgentType, AgentRunStatus

logger = structlog.get_logger()


async def seed_demo_data():
    """Seed initial demo data into PostgreSQL."""
    await init_db()

    async with AsyncSessionLocal() as session:
        # Check if already seeded
        result = await session.execute(select(Account).limit(1))
        existing_acc = result.scalars().first()
        if existing_acc:
            logger.info("ℹ️ Database already contains data. Skipping seed.")
            return

        logger.info("🌱 Seeding Google Ads demo data...")

        # 1. Create Demo Customer Account
        account = Account(
            customer_id="123-456-7890",
            name="Google Ads Demo Account (India)",
            currency_code="INR",
            time_zone="Asia/Kolkata",
            is_demo=True
        )
        session.add(account)
        await session.flush()

        # 2. Create Sample Campaigns
        c1 = Campaign(
            account_id=account.id,
            resource_name=f"customers/{account.customer_id}/campaigns/1001",
            name="Search - AI Cloud Platform India",
            status=CampaignStatus.ENABLED,
            campaign_type=CampaignType.SEARCH,
            bidding_strategy=BiddingStrategy.TARGET_CPA,
            daily_budget_micros=5000000000,  # 5,000 INR
            campaign_goal="LEADS",
            target_locations=["Hyderabad", "Bengaluru", "Mumbai", "Delhi"],
            target_languages=["English"],
            optimization_score=92.5,
            ai_brief="Search campaign for enterprise AI cloud platform targeting tech hubs in India."
        )

        c2 = Campaign(
            account_id=account.id,
            resource_name=f"customers/{account.customer_id}/campaigns/1002",
            name="Performance Max - Lead Gen South",
            status=CampaignStatus.ENABLED,
            campaign_type=CampaignType.PERFORMANCE_MAX,
            bidding_strategy=BiddingStrategy.MAXIMIZE_CONVERSIONS,
            daily_budget_micros=8000000000,  # 8,000 INR
            campaign_goal="SALES",
            target_locations=["Hyderabad", "Chennai", "Bengaluru"],
            target_languages=["English", "Telugu", "Tamil"],
            optimization_score=88.0,
            ai_brief="Performance Max campaign driving signups across Google Search, YouTube, and Display."
        )

        c3 = Campaign(
            account_id=account.id,
            resource_name=f"customers/{account.customer_id}/campaigns/1003",
            name="Search - Developer API Tools",
            status=CampaignStatus.ENABLED,
            campaign_type=CampaignType.SEARCH,
            bidding_strategy=BiddingStrategy.TARGET_ROAS,
            daily_budget_micros=4000000000,  # 4,000 INR
            campaign_goal="WEBSITE_TRAFFIC",
            target_locations=["India"],
            target_languages=["English"],
            optimization_score=96.0,
            ai_brief="Search campaign targeting API developers looking for Google Ads SDK automation tools."
        )

        session.add_all([c1, c2, c3])
        await session.flush()

        # 3. Create Ad Groups for Campaign 1
        ag1 = AdGroup(
            campaign_id=c1.id,
            resource_name=f"customers/{account.customer_id}/adGroups/2001",
            name="Core Cloud Platform Keywords",
            status=AdGroupStatus.ENABLED,
            cpc_bid_micros=45000000,  # 45 INR
            target_cpa_micros=500000000,  # 500 INR
            quality_score=9
        )
        session.add(ag1)
        await session.flush()

        # 4. Create Keywords
        kw1 = Keyword(ad_group_id=ag1.id, text="ai cloud platform india", match_type=KeywordMatchType.EXACT, bid_micros=45000000, quality_score=9)
        kw2 = Keyword(ad_group_id=ag1.id, text="enterprise ads api automation", match_type=KeywordMatchType.PHRASE, bid_micros=50000000, quality_score=10)
        kw3 = Keyword(ad_group_id=ag1.id, text="multi agent cloud tools", match_type=KeywordMatchType.BROAD, bid_micros=35000000, quality_score=8)
        session.add_all([kw1, kw2, kw3])

        # 5. Create Responsive Search Ad (RSA)
        ad1 = Ad(
            ad_group_id=ag1.id,
            resource_name=f"customers/{account.customer_id}/adGroupAds/3001",
            ad_type=AdType.RESPONSIVE_SEARCH_AD,
            headlines=[
                "AI Cloud Platform India",
                "Automate Google Ads API",
                "Enterprise Agent Automation",
                "Scale Campaign ROAS Today",
                "Try AdsIQ Platform Free"
            ],
            descriptions=[
                "Transform your ad campaigns with multi-agent AI intelligence. Built for developers & teams.",
                "Automate GAQL reporting, troubleshoot API errors instantly, and boost conversion rates."
            ],
            final_urls=["https://adsiq.example.com"],
            display_url="adsiq.example.com/cloud",
            policy_status="ELIGIBLE",
            ai_generated=True
        )
        session.add(ad1)

        # 6. Generate 14 days of time-series Performance Metrics for all campaigns
        now = datetime.utcnow()
        for i in range(14, 0, -1):
            metric_date = now - timedelta(days=i)
            for camp in [c1, c2, c3]:
                base_imp = random.randint(15000, 35000)
                base_clicks = int(base_imp * random.uniform(0.03, 0.08))
                cost = base_clicks * random.randint(35, 55) * 1000000  # micros
                conversions = float(int(base_clicks * random.uniform(0.04, 0.10)))
                conv_val = conversions * random.uniform(800, 1500)

                pm = PerformanceMetric(
                    campaign_id=camp.id,
                    date=metric_date,
                    impressions=base_imp,
                    clicks=base_clicks,
                    cost_micros=cost,
                    conversions=conversions,
                    conversion_value=conv_val,
                    ctr=round(base_clicks / base_imp, 4),
                    average_cpc_micros=int(cost / max(base_clicks, 1)),
                    roas=round(conv_val / max(cost / 1000000, 1), 2),
                    impression_share=round(random.uniform(0.65, 0.92), 2)
                )
                session.add(pm)

        # 7. Seed Sample Agent Run Log
        agent_run = AgentRun(
            agent_type=AgentType.TROUBLESHOOTER,
            status=AgentRunStatus.COMPLETED,
            input_data={"error_code": "AUTHENTICATION_ERROR.OAUTH_TOKEN_EXPIRED"},
            output_data={"status": "DIAGNOSED", "fix": "Refreshed OAuth credentials"},
            tokens_used=380,
            estimated_cost_cents=0.12,
            duration_ms=420
        )
        session.add(agent_run)

        await session.commit()
        logger.info("✅ Demo data seeded successfully!")


if __name__ == "__main__":
    asyncio.run(seed_demo_data())
