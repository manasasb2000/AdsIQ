# ============================================================
# backend/app/schemas/analytics.py
# ============================================================

from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional

class GAQLQueryRequest(BaseModel):
    query: str = Field(..., description="GAQL Query string (e.g. SELECT campaign.name, metrics.clicks FROM campaign)")
    customer_id: Optional[str] = Field("123-456-7890", description="Google Ads Customer ID")

class GAQLQueryResponse(BaseModel):
    query: str
    row_count: int
    results: List[Dict[str, Any]]
    execution_time_ms: float

class AnalyticsDashboardResponse(BaseModel):
    total_campaigns: int
    active_campaigns: int
    total_impressions: int
    total_clicks: int
    total_cost_inr: float
    total_conversions: float
    average_ctr: float
    average_cpc_inr: float
    average_roas: float
    average_quality_score: float
    chart_series: List[Dict[str, Any]]
