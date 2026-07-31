# ============================================================
# backend/app/api/v1/analytics.py
# ============================================================

from fastapi import APIRouter
from app.schemas.analytics import GAQLQueryRequest, GAQLQueryResponse, AnalyticsDashboardResponse
from app.ads_api_sim.gaql_engine import gaql_engine

router = APIRouter()


@router.post("/gaql", response_model=GAQLQueryResponse)
async def execute_gaql(request: GAQLQueryRequest):
    """Execute a raw GAQL statement against the simulated Google Ads dataset."""
    results, exec_time = gaql_engine.execute_query(request.query)
    return GAQLQueryResponse(
        query=request.query,
        row_count=len(results),
        results=results,
        execution_time_ms=exec_time
    )


@router.get("/dashboard", response_model=AnalyticsDashboardResponse)
async def get_analytics_dashboard():
    """Retrieve high-level Google Ads API metrics and time-series chart data."""
    return AnalyticsDashboardResponse(
        total_campaigns=4,
        active_campaigns=3,
        total_impressions=1138500,
        total_clicks=36470,
        total_cost_inr=1637500.0,
        total_conversions=1727.0,
        average_ctr=3.20,
        average_cpc_inr=44.90,
        average_roas=4.67,
        average_quality_score=8.25,
        chart_series=[
            {"date": "Jul 24", "impressions": 140000, "clicks": 4200, "cost": 180000, "conversions": 190},
            {"date": "Jul 25", "impressions": 165000, "clicks": 5100, "cost": 220000, "conversions": 240},
            {"date": "Jul 26", "impressions": 180000, "clicks": 5800, "cost": 260000, "conversions": 280},
            {"date": "Jul 27", "impressions": 195000, "clicks": 6400, "cost": 290000, "conversions": 310},
            {"date": "Jul 28", "impressions": 210000, "clicks": 7100, "cost": 320000, "conversions": 340},
            {"date": "Jul 29", "impressions": 248500, "clicks": 7870, "cost": 367500, "conversions": 367},
        ]
    )
