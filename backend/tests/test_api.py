# ============================================================
# backend/tests/test_api.py
# ============================================================

import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_root_endpoint():
    """Test root health check."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "AdsIQ — Google Ads API Intelligence Platform"
    assert data["status"] == "operational"


def test_health_endpoint():
    """Test detailed health check."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_troubleshoot_oauth_error():
    """Test API Troubleshooter error diagnosis."""
    payload = {
        "error_code": "AUTHENTICATION_ERROR.OAUTH_TOKEN_EXPIRED",
        "programming_language": "python"
    }
    response = client.post("/api/v1/troubleshoot/", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["found"] is True
    assert data["category"] == "Authentication"
    assert "Credentials" in data["code_fix"]


def test_creative_rsa_limits():
    """Test Creative Studio RSA headline character limits."""
    payload = {
        "product_name": "CloudSync AI",
        "product_description": "Enterprise Google Ads API automation platform."
    }
    response = client.post("/api/v1/creative/generate", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert len(data["headlines"]) == 15
    assert len(data["descriptions"]) == 4
    for h in data["headlines"]:
        assert len(h) <= 30
    for d in data["descriptions"]:
        assert len(d) <= 90


def test_gaql_engine_query():
    """Test GAQL reporting query execution."""
    payload = {
        "query": "SELECT campaign.name, metrics.clicks FROM campaign"
    }
    response = client.post("/api/v1/analytics/gaql", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["row_count"] > 0
    assert "metrics.clicks" in data["results"][0]


def test_agent_workflow_execution():
    """Test LangGraph Agent State Machine execution."""
    payload = {
        "agent_type": "TROUBLESHOOTER",
        "prompt": "Fix AUTHENTICATION_ERROR.OAUTH_TOKEN_EXPIRED error"
    }
    response = client.post("/api/v1/agents/run", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "COMPLETED"
    assert "troubleshooter_result" in data["output_data"]
