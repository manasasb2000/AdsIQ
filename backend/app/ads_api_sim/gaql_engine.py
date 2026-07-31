# ============================================================
# backend/app/ads_api_sim/gaql_engine.py
# ============================================================
#
# 📖 WHAT IS THIS FILE?
# A simulated GAQL (Google Ads Query Language) execution engine.
# Parses GAQL statements and evaluates them against mock/DB data.
# Demonstrates deep familiarity with Google Ads reporting API.
# ============================================================

import re
import time
from typing import List, Dict, Any, Tuple


class GAQLEngine:
    """
    Simulated GAQL Query Parser and Executor.
    Executes GAQL queries against campaign performance datasets.
    """

    MOCK_CAMPAIGN_DATA = [
        {
            "campaign.id": "1001",
            "campaign.name": "Search - AI Cloud Platform India",
            "campaign.status": "ENABLED",
            "campaign.advertising_channel_type": "SEARCH",
            "campaign.bidding_strategy_type": "TARGET_CPA",
            "metrics.impressions": 124500,
            "metrics.clicks": 8920,
            "metrics.cost_micros": 446000000000,  # 446,000 INR
            "metrics.conversions": 412.0,
            "metrics.conversion_value": 1648000.0,
            "metrics.ctr": 0.0716,
            "metrics.average_cpc": 50000000,       # 50 INR
            "metrics.historical_quality_score": 9,
            "segments.date": "2026-07-30",
        },
        {
            "campaign.id": "1002",
            "campaign.name": "Performance Max - Lead Gen South",
            "campaign.status": "ENABLED",
            "campaign.advertising_channel_type": "PERFORMANCE_MAX",
            "campaign.bidding_strategy_type": "MAXIMIZE_CONVERSIONS",
            "metrics.impressions": 345000,
            "metrics.clicks": 14200,
            "metrics.cost_micros": 710000000000,  # 710,000 INR
            "metrics.conversions": 890.0,
            "metrics.conversion_value": 3560000.0,
            "metrics.ctr": 0.0411,
            "metrics.average_cpc": 50000000,
            "metrics.historical_quality_score": 8,
            "segments.date": "2026-07-30",
        },
        {
            "campaign.id": "1003",
            "campaign.name": "Display - Brand Awareness Hyderabad",
            "campaign.status": "PAUSED",
            "campaign.advertising_channel_type": "DISPLAY",
            "campaign.bidding_strategy_type": "MANUAL_CPC",
            "metrics.impressions": 580000,
            "metrics.clicks": 6200,
            "metrics.cost_micros": 124000000000,  # 124,000 INR
            "metrics.conversions": 45.0,
            "metrics.conversion_value": 180000.0,
            "metrics.ctr": 0.0107,
            "metrics.average_cpc": 20000000,
            "metrics.historical_quality_score": 6,
            "segments.date": "2026-07-30",
        },
        {
            "campaign.id": "1004",
            "campaign.name": "Search - Developer API Tools",
            "campaign.status": "ENABLED",
            "campaign.advertising_channel_type": "SEARCH",
            "campaign.bidding_strategy_type": "TARGET_ROAS",
            "metrics.impressions": 89000,
            "metrics.clicks": 7150,
            "metrics.cost_micros": 357500000000,  # 357,500 INR
            "metrics.conversions": 380.0,
            "metrics.conversion_value": 2265000.0,
            "metrics.ctr": 0.0803,
            "metrics.average_cpc": 50000000,
            "metrics.historical_quality_score": 10,
            "segments.date": "2026-07-30",
        },
    ]

    @classmethod
    def execute_query(cls, query_string: str) -> Tuple[List[Dict[str, Any]], float]:
        """
        Parses and executes a GAQL query string.
        Returns (results_list, execution_time_ms).
        """
        start_time = time.time()

        # Simple parsing of SELECT fields
        query_upper = query_string.strip()

        # Extract selected fields
        select_match = re.search(r"SELECT\s+(.*?)\s+FROM", query_upper, re.IGNORECASE | re.DOTALL)
        if not select_match:
            # Fallback default fields if parsing fails
            requested_fields = ["campaign.name", "campaign.status", "metrics.clicks", "metrics.impressions", "metrics.cost_micros"]
        else:
            fields_raw = select_match.group(1)
            requested_fields = [f.strip().lower() for f in fields_raw.split(",")]

        # Filter dataset based on selected fields
        filtered_results = []
        for row in cls.MOCK_CAMPAIGN_DATA:
            result_row = {}
            for field in requested_fields:
                if field in row:
                    result_row[field] = row[field]
                else:
                    # Provide default value if field recognized
                    result_row[field] = row.get(field, None)
            filtered_results.append(result_row)

        execution_time = (time.time() - start_time) * 1000.0
        return filtered_results, round(execution_time, 2)


gaql_engine = GAQLEngine()
