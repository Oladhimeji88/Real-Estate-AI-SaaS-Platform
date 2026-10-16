const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8000";

export type InsightsResponse = {
  city: string;
  price_trend: Array<{ month: string; avg_price: number }>;
  demand_heatmap: Array<{ zip_code: string; demand_index: number }>;
  predictions: {
    next_30_day_avg_price: number;
    inventory_direction: string;
  };
};

export type TrustScoreResponse = {
  agent_id: string;
  trust_score: number;
  breakdown: {
    posting_quality: number;
    response_rate: number;
    historical_accuracy: number;
  };
};

export type EstimatePricePayload = {
  location_score: number;
  sqft: number;
  beds: number;
  baths: number;
  amenities_score: number;
  market_index: number;
};

export type EstimatePriceResponse = {
  estimated_price_range: {
    min: number;
    max: number;
  };
  confidence_score: number;
  model: string;
};

const defaultEstimatePricePayload: EstimatePricePayload = {
  location_score: 0.82,
  sqft: 2100,
  beds: 3,
  baths: 2.5,
  amenities_score: 0.73,
  market_index: 1.04
};

async function fetchJson<T>(path: string, init?: RequestInit): Promise<T> {
  const res = await fetch(`${API_BASE_URL}${path}`, {
    cache: "no-store",
    ...init
  });

  if (!res.ok) {
    const responseBody = await res.text().catch(() => "");
    const details = responseBody ? ` - ${responseBody}` : "";
    throw new Error(`Request failed (${res.status}) for ${path}${details}`);
  }

  return res.json() as Promise<T>;
}

export function getInsights(city = "Austin") {
  const query = new URLSearchParams({ city }).toString();
  return fetchJson<InsightsResponse>(`/api/insights?${query}`);
}

export function getTrustScore(agentId: string) {
  return fetchJson<TrustScoreResponse>(`/api/agents/${encodeURIComponent(agentId)}/trust-score`);
}

export function estimatePrice(payload: EstimatePricePayload = defaultEstimatePricePayload) {
  return fetchJson<EstimatePriceResponse>("/api/ai/estimate-price", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload)
  });
}
