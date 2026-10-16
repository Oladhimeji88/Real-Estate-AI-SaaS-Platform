import { estimatePrice, getInsights, getTrustScore } from "../lib/api";

export default async function Page() {
  const [insightsResult, trustResult, priceResult] = await Promise.allSettled([
    getInsights(),
    getTrustScore("agent-001"),
    estimatePrice()
  ]);

  const insights = insightsResult.status === "fulfilled" ? insightsResult.value : null;
  const trust = trustResult.status === "fulfilled" ? trustResult.value : null;
  const price = priceResult.status === "fulfilled" ? priceResult.value : null;

  return (
    <main>
      <h1>RealEstate Intelligence Suite</h1>
      <p style={{ color: "var(--muted)", marginTop: 0 }}>AI market analytics, fraud checks, and trust signals.</p>

      <section className="grid" style={{ marginTop: 16 }}>
        <article className="card">
          <div className="label">Trust Score</div>
          {trust ? (
            <>
              <div className="value">{trust.trust_score}</div>
              <div className="label">Agent: {trust.agent_id}</div>
            </>
          ) : (
            <div className="label">Unavailable right now</div>
          )}
        </article>

        <article className="card">
          <div className="label">Estimated Price Range</div>
          {price ? (
            <>
              <div className="value">${price.estimated_price_range.min.toLocaleString()} - ${price.estimated_price_range.max.toLocaleString()}</div>
              <div className="label">Confidence: {price.confidence_score}</div>
            </>
          ) : (
            <div className="label">Unavailable right now</div>
          )}
        </article>

        <article className="card">
          <div className="label">Next 30-Day Avg Price</div>
          {insights ? (
            <>
              <div className="value">${insights.predictions.next_30_day_avg_price.toLocaleString()}</div>
              <div className="label">Inventory: {insights.predictions.inventory_direction}</div>
            </>
          ) : (
            <div className="label">Unavailable right now</div>
          )}
        </article>
      </section>

      <section className="card" style={{ marginTop: 14 }}>
        <div className="label" style={{ marginBottom: 8 }}>Price Trend JSON</div>
        <pre>{JSON.stringify(insights?.price_trend ?? { error: "Insights unavailable" }, null, 2)}</pre>
      </section>
    </main>
  );
}
