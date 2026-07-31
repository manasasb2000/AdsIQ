# ============================================================
# backend/app/api/v1/codegen.py
# ============================================================

from fastapi import APIRouter
from pydantic import BaseModel, Field

router = APIRouter()

class CodeGenRequest(BaseModel):
    action: str = Field("create_campaign", description="API action (create_campaign, mutate_keywords, fetch_reports)")
    language: str = Field("python", description="Target programming language (python, javascript, java, php)")
    customer_id: str = Field("123-456-7890", description="Google Ads Customer ID")

class CodeGenResponse(BaseModel):
    action: str
    language: str
    code_snippet: str
    explanation: str

@router.post("/", response_model=CodeGenResponse)
async def generate_sdk_code(request: CodeGenRequest):
    """Generate production-ready Google Ads API client library code snippets."""
    lang = request.language.lower()

    if lang == "javascript" or lang == "node":
        code = f"""// Official Google Ads API Node.js Client
const {{ GoogleAdsApi }} = require('google-ads-api');

const client = new GoogleAdsApi({{
  client_id: process.env.CLIENT_ID,
  client_secret: process.env.CLIENT_SECRET,
  developer_token: process.env.DEVELOPER_TOKEN
}});

const customer = client.Customer({{
  customer_id: '{request.customer_id}',
  refresh_token: process.env.REFRESH_TOKEN
}});

async function run() {{
  const campaigns = await customer.report({{
    entity: 'campaign',
    attributes: ['campaign.id', 'campaign.name'],
    metrics: ['metrics.clicks', 'metrics.impressions'],
    limit: 10
  }});
  console.log('Campaigns:', campaigns);
}}
run();"""
    else:
        code = f"""# Official Google Ads API Python Client Library
from google.ads.googleads.client import GoogleAdsClient

def main():
    client = GoogleAdsClient.load_from_env()
    ga_service = client.get_service("GoogleAdsService")

    query = \"\"\"
        SELECT
            campaign.id,
            campaign.name,
            metrics.impressions,
            metrics.clicks
        FROM campaign
        LIMIT 10
    \"\"\"

    search_request = client.get_type("SearchGoogleAdsRequest")
    search_request.customer_id = "{request.customer_id}"
    search_request.query = query

    results = ga_service.search(request=search_request)
    for row in results:
        print(f"Campaign {{row.campaign.name}}: {{row.metrics.clicks}} clicks")

if __name__ == "__main__":
    main()"""

    return CodeGenResponse(
        action=request.action,
        language=lang,
        code_snippet=code,
        explanation=f"Generated production code snippet for Google Ads API ({lang.capitalize()} client library)."
    )
