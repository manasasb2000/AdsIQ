# 📖 Google Ads API Technical Guide & Troubleshooting Handbook

This guide demonstrates key technical concepts required for the **Product Solutions Engineer, Ads API** role at Google.

---

## 1. Object Hierarchy
```
Manager Account (MCC)
  └── Customer Account (123-456-7890)
        └── Campaign (Search / Display / Performance Max)
              └── Ad Group
                    ├── Keywords (EXACT / PHRASE / BROAD)
                    └── Ads (Responsive Search Ads - RSA)
```

---

## 2. Standard Bidding Strategies

| Strategy | Type | Best For |
|---|---|---|
| `MANUAL_CPC` | Manual | Full control over individual keyword bids |
| `TARGET_CPA` | Smart Bidding | Automated bidding to maintain target cost-per-action |
| `TARGET_ROAS` | Smart Bidding | Maximize revenue while maintaining target return-on-ad-spend |
| `MAXIMIZE_CONVERSIONS` | Smart Bidding | Spend full daily budget to get maximum volume of conversions |

---

## 3. Top Google Ads API Errors & Fixes

### A. `AUTHENTICATION_ERROR.OAUTH_TOKEN_EXPIRED`
- **Cause**: OAuth refresh token revoked or inactive >6 months.
- **Fix**: Re-run OAuth authorization flow; inspect `request_id` in logs.

### B. `QUOTA_ERROR.RESOURCE_EXHAUSTED`
- **Cause**: Exceeded operations per minute limit.
- **Fix**: Batch mutations (`mutate_campaigns` up to 2000 operations per request).

### C. `REQUEST_ERROR.INVALID_FIELD_NAME`
- **Cause**: Typo in GAQL field name or non-selectable field for resource.
- **Fix**: Verify query against Google Ads Query Builder tool.
