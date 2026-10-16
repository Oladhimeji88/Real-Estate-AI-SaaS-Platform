from fastapi import FastAPI

app = FastAPI(title="Insights Service", version="0.1.0")

@app.get("/api/insights")
def get_insights(city: str = "Austin"):
    return {
        "city": city,
        "price_trend": [
            {"month": "2025-09", "avg_price": 428000},
            {"month": "2025-10", "avg_price": 431500},
            {"month": "2025-11", "avg_price": 436200},
            {"month": "2025-12", "avg_price": 434100},
            {"month": "2026-01", "avg_price": 440300},
        ],
        "demand_heatmap": [
            {"zip_code": "78701", "demand_index": 0.89},
            {"zip_code": "78702", "demand_index": 0.77},
            {"zip_code": "78704", "demand_index": 0.81},
        ],
        "predictions": {
            "next_30_day_avg_price": 444800,
            "inventory_direction": "slightly_down",
        },
    }

@app.get('/health')
def health():
    return {"status": "ok", "service": "insights"}
