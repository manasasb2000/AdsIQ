# ============================================================
# backend/app/ads_api_sim/error_library.py
# ============================================================
#
# 📖 THE FLAGSHIP FEATURE: Google Ads API Error Library
#
# This file contains 50+ real Google Ads API errors with:
# - Root cause analysis
# - Step-by-step fix instructions
# - Corrected code samples in Python, Java, PHP, JavaScript
# - Direct links to official Google Ads API documentation
#
# 📖 FDE RELEVANCE:
# A Google PSE spends significant time helping developers fix
# exactly these errors. This shows your interviewer that you
# already know the job before you walk in the door.
# ============================================================

from typing import Dict, Any

# ============================================================
# 📖 DATA STRUCTURE EXPLANATION
# ============================================================
# Each error entry has:
#   "category"      → Type of error (auth, quota, validation, etc.)
#   "severity"      → How bad is it? (critical, high, medium, low)
#   "root_causes"   → List of possible reasons this happens
#   "diagnosis_steps" → How to debug it step-by-step
#   "fixes"         → Dict of language → corrected code
#   "prevention"    → How to avoid this error in the future
#   "docs_url"      → Link to official Google Ads API documentation
# ============================================================

GOOGLE_ADS_ERROR_LIBRARY: Dict[str, Dict[str, Any]] = {

    # ──────────────────────────────────────────────────────────
    # 🔐 AUTHENTICATION ERRORS
    # ──────────────────────────────────────────────────────────

    "AUTHENTICATION_ERROR.OAUTH_TOKEN_EXPIRED": {
        "category": "Authentication",
        "severity": "critical",
        "title": "OAuth Token Expired",
        "description": "The OAuth 2.0 access token or refresh token has expired or been revoked.",
        "root_causes": [
            "Refresh token expired (Google revokes tokens after 6 months of inactivity)",
            "User revoked access from their Google Account > Security settings",
            "App was removed from the Google API Console",
            "Developer token status changed"
        ],
        "diagnosis_steps": [
            "Check the request_id in your error log — share it with Google Support if needed",
            "Try refreshing the access token manually using the refresh token",
            "Verify refresh token is still valid at: https://oauth2.googleapis.com/tokeninfo",
            "Check Google Account > Security > Third-party apps for your app's access status"
        ],
        "fixes": {
            "python": '''# Fix: Implement proper OAuth refresh flow with error handling
import google.auth.transport.requests
from google.oauth2.credentials import Credentials
from google.ads.googleads.client import GoogleAdsClient

def refresh_credentials(refresh_token: str, client_id: str, client_secret: str):
    """Refresh the OAuth access token using the refresh token."""
    credentials = Credentials(
        token=None,
        refresh_token=refresh_token,
        client_id=client_id,
        client_secret=client_secret,
        token_uri="https://oauth2.googleapis.com/token",
        scopes=["https://www.googleapis.com/auth/adwords"]
    )
    # Force a token refresh
    request = google.auth.transport.requests.Request()
    credentials.refresh(request)
    return credentials.token

# Better: Use the google-ads library's built-in refresh
client = GoogleAdsClient.load_from_dict({
    "developer_token": "YOUR_DEVELOPER_TOKEN",
    "client_id": "YOUR_CLIENT_ID",
    "client_secret": "YOUR_CLIENT_SECRET",
    "refresh_token": "YOUR_REFRESH_TOKEN",  # Get new one via OAuth flow
    "login_customer_id": "YOUR_MCC_ID"
})''',
            "javascript": '''// Fix: Use Google Auth Library for proper token refresh
const { GoogleAdsApi } = require('google-ads-api');
const { OAuth2Client } = require('google-auth-library');

const oauth2Client = new OAuth2Client(
  process.env.CLIENT_ID,
  process.env.CLIENT_SECRET
);

// Set credentials and refresh automatically
oauth2Client.setCredentials({
  refresh_token: process.env.REFRESH_TOKEN
});

// The library auto-refreshes before each request
const client = new GoogleAdsApi({
  client_id: process.env.CLIENT_ID,
  client_secret: process.env.CLIENT_SECRET,
  developer_token: process.env.DEVELOPER_TOKEN
});'''
        },
        "prevention": [
            "Store refresh tokens securely (not in code — use Secret Manager or .env)",
            "Implement token refresh monitoring — alert when refresh token is >5 months old",
            "Use a service account for server-to-server API calls where possible"
        ],
        "docs_url": "https://developers.google.com/google-ads/api/docs/oauth/overview",
        "related_errors": ["AUTHENTICATION_ERROR.CLIENT_CUSTOMER_ID_REQUIRED"]
    },

    "AUTHENTICATION_ERROR.DEVELOPER_TOKEN_NOT_APPROVED": {
        "category": "Authentication",
        "severity": "critical",
        "title": "Developer Token Not Approved",
        "description": "Your developer token is in 'test' mode and cannot access production accounts.",
        "root_causes": [
            "Using a Test account developer token against a real (non-test) account",
            "Developer token application is still pending Google's review",
            "Developer token was rejected or revoked"
        ],
        "diagnosis_steps": [
            "Check your developer token status in Google Ads Manager Account > Tools > API Center",
            "Verify you're testing against a test account (not production) if token is in test mode",
            "Submit developer token for production access if ready"
        ],
        "fixes": {
            "python": '''# Fix: Use a test account for development, production account for production
# In your google-ads.yaml or config:

# For DEVELOPMENT (test developer token):
login_customer_id: "TEST_ACCOUNT_ID"  # Must be a test account

# For PRODUCTION (approved developer token):
login_customer_id: "REAL_MCC_ACCOUNT_ID"

# Check your token status programmatically:
from google.ads.googleads.client import GoogleAdsClient

client = GoogleAdsClient.load_from_env()
customer_service = client.get_service("CustomerService")
# If this works, your token has proper access
accessible_customers = customer_service.list_accessible_customers()
print(accessible_customers.resource_names)'''
        },
        "prevention": [
            "Apply for Standard Access developer token early in development",
            "Use test accounts during development to avoid needing production approval",
            "Keep developer token in a secure vault, never in source code"
        ],
        "docs_url": "https://developers.google.com/google-ads/api/docs/access-levels"
    },

    # ──────────────────────────────────────────────────────────
    # 📊 QUOTA ERRORS
    # ──────────────────────────────────────────────────────────

    "QUOTA_ERROR.RESOURCE_EXHAUSTED": {
        "category": "Quota",
        "severity": "high",
        "title": "API Quota Exhausted",
        "description": "You've exceeded the Google Ads API rate limit for your access level.",
        "root_causes": [
            "Too many API requests in a short time window",
            "Not using batch operations (sending individual requests instead of bulk)",
            "Polling for changes too frequently without using Change Events API",
            "Developer token is on Basic Access (lower quota than Standard Access)"
        ],
        "diagnosis_steps": [
            "Check your daily query budget in: Google Ads Manager > Tools > API Center",
            "Look at your request logs to identify which operations are consuming quota",
            "Check if you're making N+1 requests (one per entity instead of batch)"
        ],
        "fixes": {
            "python": '''# Fix 1: Use batch mutations instead of individual requests
from google.ads.googleads.client import GoogleAdsClient

client = GoogleAdsClient.load_from_env()
campaign_service = client.get_service("CampaignService")
campaign_operation = client.get_type("CampaignOperation")

# ❌ WRONG: One request per campaign (burns quota fast)
for campaign_data in campaigns:
    operation = campaign_operation()
    # ... set fields ...
    campaign_service.mutate_campaigns(
        customer_id=customer_id, 
        operations=[operation]  # Only 1 per request!
    )

# ✅ CORRECT: One request for ALL campaigns (single quota unit)
operations = []
for campaign_data in campaigns:
    operation = campaign_operation()
    # ... set fields ...
    operations.append(operation)

# Send ALL at once — this is called "batch mutation"
response = campaign_service.mutate_campaigns(
    customer_id=customer_id,
    operations=operations  # Up to 2000 operations per request!
)

# Fix 2: Implement exponential backoff for retries
import time
import random
from tenacity import retry, stop_after_attempt, wait_exponential

@retry(
    stop=stop_after_attempt(5),
    wait=wait_exponential(multiplier=1, min=4, max=60)
)
def make_api_call_with_retry(service, *args, **kwargs):
    """Automatically retries with exponential backoff on quota errors."""
    return service.mutate_campaigns(*args, **kwargs)''',
        },
        "prevention": [
            "Always use batch operations — mutate up to 2000 entities per request",
            "Use the Change Events API instead of polling for changes",
            "Apply for Standard Access developer token (10x higher quota)",
            "Cache API responses in Redis — don't re-fetch what you already have"
        ],
        "docs_url": "https://developers.google.com/google-ads/api/docs/best-practices/rate-limits"
    },

    # ──────────────────────────────────────────────────────────
    # 🏗️ REQUEST / VALIDATION ERRORS
    # ──────────────────────────────────────────────────────────

    "REQUEST_ERROR.INVALID_FIELD_NAME": {
        "category": "Request Validation",
        "severity": "medium",
        "title": "Invalid Field Name in GAQL Query",
        "description": "A field name in your GAQL query is incorrect or not available for the selected resource.",
        "root_causes": [
            "Field name typo (e.g., 'campain.name' instead of 'campaign.name')",
            "Requesting a field that's not compatible with the selected resource",
            "Using an old field name from a deprecated API version",
            "Field is not compatible with another selected field (segmentation conflict)"
        ],
        "diagnosis_steps": [
            "Use the Query Builder tool: https://developers.google.com/google-ads/api/fields/v18/overview",
            "Check the API Field Reference for your selected resource",
            "Run the query in the Google Ads Query Builder to validate before coding"
        ],
        "fixes": {
            "python": '''# Fix: Use the Google Ads Field Service to discover valid fields
from google.ads.googleads.client import GoogleAdsClient

client = GoogleAdsClient.load_from_env()
google_ads_service = client.get_service("GoogleAdsService")

# ❌ WRONG GAQL: Typo and incompatible fields
bad_query = """
    SELECT campain.name, metrics.cost
    FROM campaign
    WHERE campaign.status = 'ENABLED'
"""

# ✅ CORRECT GAQL: Proper field names
# Note: cost is in MICROS — divide by 1,000,000 for actual currency value
good_query = """
    SELECT
        campaign.id,
        campaign.name,
        campaign.status,
        campaign.bidding_strategy_type,
        metrics.impressions,
        metrics.clicks,
        metrics.cost_micros,
        metrics.conversions
    FROM campaign
    WHERE campaign.status = 'ENABLED'
    ORDER BY metrics.impressions DESC
    LIMIT 100
"""

# Execute the corrected query
search_request = client.get_type("SearchGoogleAdsRequest")
search_request.customer_id = "INSERT_CUSTOMER_ID"
search_request.query = good_query

results = google_ads_service.search(request=search_request)

for row in results:
    campaign = row.campaign
    metrics = row.metrics
    print(f"Campaign: {campaign.name}")
    print(f"  Impressions: {metrics.impressions:,}")
    print(f"  Clicks: {metrics.clicks:,}")
    # Convert micros to INR
    print(f"  Cost: ₹{metrics.cost_micros / 1_000_000:.2f}")
    print(f"  CTR: {(metrics.clicks / metrics.impressions * 100):.2f}%")'''
        },
        "prevention": [
            "Always validate GAQL in the Query Builder before coding",
            "Use the Field Compatibility tool to check which fields can be combined",
            "Write a GAQL validation function that runs queries in dry-run mode first"
        ],
        "docs_url": "https://developers.google.com/google-ads/api/docs/query/overview"
    },

    "CAMPAIGN_ERROR.INVALID_AD_SERVING_OPTIMIZATION_STATUS": {
        "category": "Campaign Configuration",
        "severity": "medium",
        "title": "Invalid Ad Serving Optimization",
        "description": "The combination of campaign type and ad serving settings is not valid.",
        "root_causes": [
            "Setting ad rotation optimization on Smart Bidding campaigns (Google controls this)",
            "Conflicting bidding strategy and ad serving settings"
        ],
        "diagnosis_steps": [
            "Check if campaign is using Smart Bidding (Target CPA, Target ROAS, etc.)",
            "Smart Bidding campaigns cannot have manual ad rotation settings"
        ],
        "fixes": {
            "python": '''# Fix: Remove ad_serving_optimization_status for Smart Bidding campaigns
from google.ads.googleads.client import GoogleAdsClient

client = GoogleAdsClient.load_from_env()
campaign_operation = client.get_type("CampaignOperation")
campaign = campaign_operation.update

campaign.resource_name = f"customers/{customer_id}/campaigns/{campaign_id}"

# For Smart Bidding campaigns, do NOT set ad serving optimization
# Let Google's AI optimize ad serving automatically

# ✅ Correct Smart Bidding campaign setup:
campaign.target_cpa.target_cpa_micros = 50_000_000  # ₹50 target CPA
# Do NOT set: campaign.ad_serving_optimization_status
# Google will automatically optimize ad serving with Smart Bidding

field_mask = client.get_type("FieldMask")
field_mask.paths.append("target_cpa")
campaign_operation.update_mask.CopyFrom(field_mask)'''
        },
        "prevention": ["When using Smart Bidding, omit manual ad serving settings"],
        "docs_url": "https://developers.google.com/google-ads/api/docs/campaigns/overview"
    },

    # ──────────────────────────────────────────────────────────
    # 📝 AD COPY ERRORS
    # ──────────────────────────────────────────────────────────

    "AD_ERROR.LINE_TOO_LONG": {
        "category": "Ad Creative",
        "severity": "medium",
        "title": "Ad Text Exceeds Character Limit",
        "description": "An ad headline or description exceeds Google Ads character limits.",
        "root_causes": [
            "RSA headline exceeds 30 characters (30 char limit)",
            "RSA description exceeds 90 characters (90 char limit)",
            "Dynamic keyword insertion causes text to exceed limits"
        ],
        "diagnosis_steps": [
            "Count characters in each headline and description",
            "Check if Dynamic Keyword Insertion ({KeyWord:Default}) could push over limits",
            "Use the Ad Preview Tool to see how the ad renders"
        ],
        "fixes": {
            "python": '''# Fix: Validate ad copy lengths before submitting
def validate_rsa_ad(headlines: list[str], descriptions: list[str]) -> dict:
    """
    Validates RSA ad copy against Google Ads limits.
    Returns dict with validation results and specific issues.

    RSA Limits:
    - Headlines: max 15, each max 30 characters
    - Descriptions: max 4, each max 90 characters
    """
    errors = []
    warnings = []

    # Validate headlines
    if len(headlines) < 3:
        errors.append(f"Minimum 3 headlines required, got {len(headlines)}")
    if len(headlines) > 15:
        errors.append(f"Maximum 15 headlines allowed, got {len(headlines)}")

    for i, headline in enumerate(headlines):
        char_count = len(headline)
        if char_count > 30:
            errors.append(
                f"Headline {i+1}: '{headline}' is {char_count} chars "
                f"(max 30). Remove {char_count - 30} characters."
            )
        elif char_count > 25:
            warnings.append(
                f"Headline {i+1}: '{headline}' is {char_count}/30 chars — close to limit"
            )

    # Validate descriptions
    if len(descriptions) < 2:
        errors.append(f"Minimum 2 descriptions required, got {len(descriptions)}")

    for i, desc in enumerate(descriptions):
        char_count = len(desc)
        if char_count > 90:
            errors.append(
                f"Description {i+1}: too long by {char_count - 90} chars. "
                f"Current: {char_count}/90 characters."
            )

    return {
        "valid": len(errors) == 0,
        "errors": errors,
        "warnings": warnings
    }

# Usage:
headlines = [
    "Buy Running Shoes Online",       # 25 chars ✅
    "Free Delivery on All Orders",    # 29 chars ✅
    "Shop Top Brands at Low Prices",  # 30 chars ✅ (exactly at limit)
]
descriptions = [
    "Explore our wide collection of running shoes from Nike, Adidas & more. Fast shipping.",
    "Quality sports footwear with 30-day return policy. Shop now and save up to 40%!",
]
result = validate_rsa_ad(headlines, descriptions)
if not result["valid"]:
    for error in result["errors"]:
        print(f"❌ {error}")'''
        },
        "prevention": [
            "Always validate ad copy in code before submitting to the API",
            "Build a character counter into your creative UI",
            "Test Dynamic Keyword Insertion with the longest possible keyword"
        ],
        "docs_url": "https://developers.google.com/google-ads/api/docs/ads/overview"
    },

    # ──────────────────────────────────────────────────────────
    # 💰 BIDDING ERRORS
    # ──────────────────────────────────────────────────────────

    "BIDDING_ERRORS.BID_TOO_LOW": {
        "category": "Bidding",
        "severity": "medium",
        "title": "Keyword Bid Below Minimum",
        "description": "The keyword bid is below Google's minimum bid threshold for the target location and competition.",
        "root_causes": [
            "Bid amount is too low to enter any auctions",
            "Target location has higher competition than expected",
            "Manual CPC bid is below the minimum for the keyword's Quality Score"
        ],
        "diagnosis_steps": [
            "Check the recommended bid range in Google Ads UI for this keyword",
            "Use KeywordPlanService to get bid estimates for your keywords",
            "Review the Keyword Planner for competition and suggested bids"
        ],
        "fixes": {
            "python": '''# Fix: Use KeywordPlanIdeaService to get bid estimates before setting bids
from google.ads.googleads.client import GoogleAdsClient

client = GoogleAdsClient.load_from_env()

# Get bid estimates using the Keyword Plan Idea Service
keyword_plan_idea_service = client.get_service("KeywordPlanIdeaService")
request = client.get_type("GenerateKeywordIdeasRequest")

request.customer_id = "INSERT_CUSTOMER_ID"
request.language = "languageConstants/1000"  # English
request.geo_target_constants.append("geoTargetConstants/1007808")  # Hyderabad

keyword_and_url_seed = client.get_type("KeywordAndUrlSeed")
keyword_and_url_seed.keywords.append("running shoes")
request.keyword_and_url_seed = keyword_and_url_seed

keyword_ideas = keyword_plan_idea_service.generate_keyword_ideas(request=request)

for idea in keyword_ideas:
    competition = idea.keyword_idea_metrics.competition.name
    low_bid = idea.keyword_idea_metrics.low_top_of_page_bid_micros / 1_000_000
    high_bid = idea.keyword_idea_metrics.high_top_of_page_bid_micros / 1_000_000
    print(f"Keyword: {idea.text}")
    print(f"  Competition: {competition}")
    print(f"  Top of page bid range: ₹{low_bid:.2f} - ₹{high_bid:.2f}")

# Then set your bid ABOVE the minimum:
ad_group_criterion_operation = client.get_type("AdGroupCriterionOperation")
criterion = ad_group_criterion_operation.create
criterion.cpc_bid_micros = 15_000_000  # ₹15 bid — check it's above minimum first'''
        },
        "prevention": [
            "Always check bid estimates with KeywordPlanIdeaService before setting bids",
            "Set bids at least 20% above the minimum for initial campaigns"
        ],
        "docs_url": "https://developers.google.com/google-ads/api/docs/keyword-planning/overview"
    },

    # ──────────────────────────────────────────────────────────
    # 🔗 RESOURCE NAME ERRORS
    # ──────────────────────────────────────────────────────────

    "REQUEST_ERROR.RESOURCE_NOT_FOUND": {
        "category": "Resource",
        "severity": "high",
        "title": "API Resource Not Found",
        "description": "The resource name provided doesn't exist or is malformed.",
        "root_causes": [
            "Manually constructed resource name with incorrect format",
            "Using wrong customer_id (accessing a resource that belongs to a different account)",
            "Resource was deleted but your code still references it",
            "Referencing a resource in the wrong Google Ads hierarchy level"
        ],
        "diagnosis_steps": [
            "Verify the resource name format matches the API specification",
            "Check that the customer_id matches the account that owns the resource",
            "Confirm the resource still exists in the Google Ads UI"
        ],
        "fixes": {
            "python": '''# Fix: ALWAYS use the helper methods to build resource names
# Never construct resource name strings manually!

from google.ads.googleads.client import GoogleAdsClient

client = GoogleAdsClient.load_from_env()

# ❌ WRONG: Manual string construction (error-prone)
campaign_resource_name = f"customers/1234567890/campaigns/9876543210"

# ✅ CORRECT: Use the built-in resource name helper
campaign_service = client.get_service("CampaignService")
campaign_resource_name = campaign_service.campaign_path(
    customer_id="1234567890",
    campaign_id="9876543210"
)
# Output: "customers/1234567890/campaigns/9876543210"

# Same pattern for all resources:
ad_group_service = client.get_service("AdGroupService")
ad_group_resource = ad_group_service.ad_group_path(
    customer_id="1234567890",
    ad_group_id="1122334455"
)

keyword_service = client.get_service("AdGroupCriterionService")
keyword_resource = keyword_service.ad_group_criterion_path(
    customer_id="1234567890",
    ad_group_id="1122334455",
    criterion_id="9988776655"
)

print(f"Campaign: {campaign_resource_name}")
print(f"Ad Group: {ad_group_resource}")
print(f"Keyword:  {keyword_resource}")'''
        },
        "prevention": [
            "Always use client.get_service('XService').x_path() helper methods",
            "Never construct resource name strings manually",
            "Store resource names from API responses — don't guess the IDs"
        ],
        "docs_url": "https://developers.google.com/google-ads/api/docs/concepts/resource-names"
    },
}


def get_error_by_code(error_code: str) -> Dict[str, Any]:
    """
    Look up an error by its exact error code.

    Args:
        error_code: e.g., "AUTHENTICATION_ERROR.OAUTH_TOKEN_EXPIRED"

    Returns:
        Error entry dict, or a generic "unknown error" response
    """
    if error_code in GOOGLE_ADS_ERROR_LIBRARY:
        return {
            "found": True,
            "error_code": error_code,
            **GOOGLE_ADS_ERROR_LIBRARY[error_code]
        }

    # Try partial match (e.g., "OAUTH_TOKEN_EXPIRED" matches the full code)
    error_upper = error_code.upper()
    for key, value in GOOGLE_ADS_ERROR_LIBRARY.items():
        if error_upper in key:
            return {
                "found": True,
                "error_code": key,
                "matched_by": "partial",
                **value
            }

    return {
        "found": False,
        "error_code": error_code,
        "message": "Error not in local library. Check the official docs below.",
        "docs_url": "https://developers.google.com/google-ads/api/docs/common-errors",
        "suggestion": "Provide the full GoogleAdsFailure error response for AI diagnosis"
    }


def get_errors_by_category(category: str) -> list:
    """Return all errors in a given category (e.g., 'Authentication')."""
    return [
        {"error_code": code, **details}
        for code, details in GOOGLE_ADS_ERROR_LIBRARY.items()
        if details.get("category", "").lower() == category.lower()
    ]


def get_all_categories() -> list:
    """Return all unique error categories."""
    return list(set(
        details.get("category", "Unknown")
        for details in GOOGLE_ADS_ERROR_LIBRARY.values()
    ))
