import os

import httpx
from fastapi import FastAPI, HTTPException, Query, Request

app = FastAPI(title="RealEstate Intelligence Suite API Gateway", version="0.1.0")

AUTH_SERVICE_URL = os.getenv("AUTH_SERVICE_URL", "http://auth-service:8001")
LISTINGS_SERVICE_URL = os.getenv("LISTINGS_SERVICE_URL", "http://listings-service:8002")
AI_SERVICE_URL = os.getenv("AI_SERVICE_URL", "http://ai-service:8003")
TRUST_SERVICE_URL = os.getenv("TRUST_SERVICE_URL", "http://trust-service:8004")
INSIGHTS_SERVICE_URL = os.getenv("INSIGHTS_SERVICE_URL", "http://insights-service:8005")
SEARCH_SERVICE_URL = os.getenv("SEARCH_SERVICE_URL", "http://search-service:8006")

async def proxy_json(method: str, url: str, payload: dict | None = None):
    async with httpx.AsyncClient(timeout=10) as client:
        response = await client.request(method, url, json=payload)
        if response.status_code >= 400:
            raise HTTPException(status_code=response.status_code, detail=response.text)
        return response.json()

@app.get('/health')
def health():
    return {"status": "ok", "service": "api-gateway"}

@app.post('/api/auth/tenants')
async def create_tenant(request: Request):
    return await proxy_json("POST", f"{AUTH_SERVICE_URL}/api/auth/tenants", await request.json())

@app.post('/api/auth/signup')
async def signup(request: Request):
    return await proxy_json("POST", f"{AUTH_SERVICE_URL}/api/auth/signup", await request.json())

@app.post('/api/auth/login')
async def login(request: Request):
    return await proxy_json("POST", f"{AUTH_SERVICE_URL}/api/auth/login", await request.json())

@app.post('/api/listings')
async def create_listing(request: Request):
    return await proxy_json("POST", f"{LISTINGS_SERVICE_URL}/api/listings", await request.json())

@app.post('/api/ai/estimate-price')
async def estimate_price(request: Request):
    return await proxy_json("POST", f"{AI_SERVICE_URL}/api/ai/estimate-price", await request.json())

@app.post('/api/ai/check-fraud')
async def check_fraud(request: Request):
    return await proxy_json("POST", f"{AI_SERVICE_URL}/api/ai/check-fraud", await request.json())

@app.get('/api/agents/{agent_id}/trust-score')
async def trust_score(agent_id: str):
    return await proxy_json("GET", f"{TRUST_SERVICE_URL}/api/agents/{agent_id}/trust-score")

@app.get('/api/insights')
async def insights(city: str = Query(default="Austin")):
    return await proxy_json("GET", f"{INSIGHTS_SERVICE_URL}/api/insights?city={city}")

@app.get('/api/search')
async def search(query: str):
    return await proxy_json("GET", f"{SEARCH_SERVICE_URL}/api/search?query={query}")
