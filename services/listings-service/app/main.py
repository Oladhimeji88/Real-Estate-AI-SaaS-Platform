from datetime import datetime
from uuid import uuid4
import os

from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from pydantic import BaseModel, Field

app = FastAPI(title="Listings Service", version="0.1.0")

S3_BUCKET = os.getenv("S3_BUCKET", "realestate-intelligence-suite-dev")

class ListingIn(BaseModel):
    tenant_id: str
    agent_id: str
    title: str
    description: str
    address: str
    city: str
    state: str
    zip_code: str
    beds: int = Field(ge=0)
    baths: float = Field(ge=0)
    sqft: int = Field(gt=0)
    amenities: list[str] = []
    listed_price: float = Field(gt=0)

listings: dict[str, dict] = {}

def text_similarity(a: str, b: str) -> float:
    a_set, b_set = set(a.lower().split()), set(b.lower().split())
    if not a_set or not b_set:
        return 0.0
    return len(a_set & b_set) / len(a_set | b_set)

def is_duplicate_candidate(payload: ListingIn) -> bool:
    for existing in listings.values():
        if existing["tenant_id"] != payload.tenant_id:
            continue
        if existing["address"].lower() == payload.address.lower():
            return True
        if text_similarity(existing["description"], payload.description) > 0.85:
            return True
    return False

@app.post("/api/listings")
def create_listing(data: ListingIn):
    duplicate = is_duplicate_candidate(data)
    listing_id = str(uuid4())
    listings[listing_id] = {
        **data.model_dump(),
        "listing_id": listing_id,
        "created_at": datetime.utcnow().isoformat(),
        "duplicate_flag": duplicate,
        "image_urls": [],
    }
    return {"listing": listings[listing_id], "validation": {"possible_duplicate": duplicate}}

@app.get("/api/listings/{listing_id}")
def get_listing(listing_id: str):
    listing = listings.get(listing_id)
    if not listing:
        raise HTTPException(status_code=404, detail="Listing not found")
    return listing

@app.put("/api/listings/{listing_id}")
def update_listing(listing_id: str, data: ListingIn):
    if listing_id not in listings:
        raise HTTPException(status_code=404, detail="Listing not found")
    listings[listing_id].update(data.model_dump())
    return listings[listing_id]

@app.delete("/api/listings/{listing_id}")
def delete_listing(listing_id: str):
    if listing_id not in listings:
        raise HTTPException(status_code=404, detail="Listing not found")
    del listings[listing_id]
    return {"deleted": True, "listing_id": listing_id}

@app.post("/api/listings/{listing_id}/images")
async def upload_listing_image(listing_id: str, file: UploadFile = File(...), tenant_id: str = Form(...)):
    if listing_id not in listings:
        raise HTTPException(status_code=404, detail="Listing not found")
    key = f"{tenant_id}/{listing_id}/{uuid4()}-{file.filename}"
    # TODO: stream to S3 with pre-signed upload in production.
    url = f"s3://{S3_BUCKET}/{key}"
    listings[listing_id]["image_urls"].append(url)
    return {"uploaded": True, "image_url": url}

@app.get('/health')
def health():
    return {"status": "ok", "service": "listings"}
