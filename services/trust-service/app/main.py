from fastapi import FastAPI

app = FastAPI(title="Trust Service", version="0.1.0")

# Replace with feature store + historical model in production.
agent_metrics = {
    "agent-001": {"posting_quality": 0.83, "response_rate": 0.91, "historical_accuracy": 0.78},
    "agent-002": {"posting_quality": 0.62, "response_rate": 0.58, "historical_accuracy": 0.71},
}

@app.get("/api/agents/{agent_id}/trust-score")
def get_trust_score(agent_id: str):
    m = agent_metrics.get(agent_id, {"posting_quality": 0.5, "response_rate": 0.5, "historical_accuracy": 0.5})
    score = round((m["posting_quality"] * 0.4 + m["response_rate"] * 0.3 + m["historical_accuracy"] * 0.3) * 100, 2)
    return {"agent_id": agent_id, "trust_score": score, "breakdown": m}

@app.get('/health')
def health():
    return {"status": "ok", "service": "trust"}
