# ============================================================
# backend/app/api/v1/creative.py
# ============================================================

from fastapi import APIRouter
from app.schemas.creative import CreativeGenerateRequest, CreativeGenerateResponse

router = APIRouter()


@router.post("/generate", response_model=CreativeGenerateResponse)
async def generate_ad_creative(request: CreativeGenerateRequest):
    """
    Generate Responsive Search Ad (RSA) copy compliant with Google Ads character limits.
    Produces 15 headlines (<=30 chars) and 4 descriptions (<=90 chars).
    """
    p_name = request.product_name

    headlines = [
        f"Buy {p_name} Online Today"[:30],
        f"Official {p_name} Store"[:30],
        f"Top Rated {p_name} 2026"[:30],
        f"Save Up To 40% On {p_name}"[:30],
        f"Fast Free Shipping Included"[:30],
        f"Easy 30 Day Return Policy"[:30],
        f"Premium Quality Guaranteed"[:30],
        f"Shop Best Deals On {p_name}"[:30],
        f"Trusted By 50,000+ Customers"[:30],
        f"Exclusive Online Offers"[:30],
        f"Order {p_name} Now"[:30],
        f"Highest Performance Choice"[:30],
        f"Certified Original Product"[:30],
        f"Limited Time Discount"[:30],
        f"Upgrade To {p_name}"[:30]
    ]

    descriptions = [
        f"Discover premium {p_name}. Designed for maximum value and performance. Order now."[:90],
        f"Get fast delivery, best price guarantee, and 24/7 customer support on all orders."[:90],
        f"Transform your workflow with {p_name}. Trusted by leading teams across India."[:90],
        f"Explore special offers and seasonal discounts. Shop official store today!"[:90]
    ]

    return CreativeGenerateResponse(
        product_name=p_name,
        headlines=headlines,
        descriptions=descriptions,
        call_to_actions=["Shop Now", "Learn More", "Get Started", "Claim Offer"],
        compliance_passed=True,
        suggestions=[
            "All headlines are under the strict 30-character Google Ads RSA limit.",
            "All descriptions comply with the 90-character limit.",
            "Include your target keywords in at least 3 headlines for a high Ad Strength rating."
        ]
    )
