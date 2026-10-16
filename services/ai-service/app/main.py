from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI(title="AI Service", version="0.1.0")

class PriceEstimateRequest(BaseModel):
    location_score: float = Field(ge=0, le=1)
    sqft: int = Field(gt=0)
    beds: int = Field(ge=0)
    baths: float = Field(ge=0)
    amenities_score: float = Field(ge=0, le=1)
    market_index: float = Field(gt=0)

class FraudCheckRequest(BaseModel):
    tenant_id: str
    listing_id: str
    title: str
    description: str
    image_hashes: list[str] = []
    posted_price: float = Field(gt=0)
    median_area_price: float = Field(gt=0)

@app.post("/api/ai/estimate-price")
def estimate_price(payload: PriceEstimateRequest):
    base_price = payload.sqft * (180 + 120 * payload.location_score)
    bedroom_adj = payload.beds * 9000
    bathroom_adj = payload.baths * 6500
    amenity_adj = 25000 * payload.amenities_score
    fair_value = (base_price + bedroom_adj + bathroom_adj + amenity_adj) * payload.market_index

    lower = round(fair_value * 0.92, 2)
    upper = round(fair_value * 1.08, 2)
    confidence = min(0.95, 0.6 + (payload.location_score + payload.amenities_score) * 0.15)

    return {
        "estimated_price_range": {"min": lower, "max": upper},
        "confidence_score": round(confidence, 3),
        "model": "baseline-regression-v1",
    }

@app.post("/api/ai/check-fraud")
def check_fraud(payload: FraudCheckRequest):
    risk = 0.0
    reasons = []

    if payload.posted_price < payload.median_area_price * 0.55:
        risk += 0.45
        reasons.append("Price is significantly below neighborhood median")

    unique_hash_ratio = len(set(payload.image_hashes)) / max(1, len(payload.image_hashes))
    if unique_hash_ratio < 0.75:
        risk += 0.3
        reasons.append("Potential duplicate/reused listing images detected")

    suspicious_keywords = ["urgent transfer", "wire only", "no viewing"]
    text_blob = f"{payload.title} {payload.description}".lower()
    if any(k in text_blob for k in suspicious_keywords):
        risk += 0.35
        reasons.append("Suspicious language pattern in listing text")

    risk_score = round(min(1.0, risk), 3)
    return {
        "listing_id": payload.listing_id,
        "risk_score": risk_score,
        "risk_level": "high" if risk_score >= 0.7 else "medium" if risk_score >= 0.4 else "low",
        "signals": reasons,
    }

@app.get('/health')
def health():
    return {"status": "ok", "service": "ai"}
