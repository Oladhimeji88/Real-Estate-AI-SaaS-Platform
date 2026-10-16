# RealEstate Intelligence Suite

Microservices-based AI SaaS platform for real estate pricing, fraud detection, trust scoring, market insights, semantic search, and real-time notifications.

## Stack
- Frontend: Next.js + TypeScript
- Backend: FastAPI microservices
- Data: PostgreSQL, Redis
- AI/ML: scikit-learn-ready service interfaces, embeddings/fraud heuristics stubs
- Cloud target: AWS (EKS, RDS, ElastiCache, S3, ECR)
- Billing: Stripe integration placeholder
- Observability: Prometheus-compatible `/metrics` stubs + structured logging

## Services
- `api-gateway` (port 8000): API entrypoint and service routing
- `auth-service` (8001): JWT auth, RBAC, tenant context
- `listings-service` (8002): Listing CRUD, image upload metadata, duplicate checks
- `ai-service` (8003): Price estimation + fraud checks
- `trust-service` (8004): Agent trust scoring
- `insights-service` (8005): Market trends and heatmap insights
- `search-service` (8006): Semantic search endpoint
- `notifications-service` (8007): WebSocket + webhook alerts
- `frontend` (3000): Dashboard starter UI

## Local Run
1. Copy envs: `Copy-Item .env.example .env`
2. Build + run: `docker compose up --build`
3. Open:
   - Frontend: http://localhost:3000
   - Gateway docs: http://localhost:8000/docs

## Required APIs (available through gateway)
- `POST /api/listings`
- `POST /api/ai/estimate-price`
- `POST /api/ai/check-fraud`
- `GET /api/agents/{agentId}/trust-score`
- `GET /api/insights`
- `GET /api/search?query=...`

## Notes
- This is an initial framework with production-oriented structure.
- Replace in-memory stores with PostgreSQL models and background workers.
- Wire cloud services (S3, Stripe, Kafka/Kinesis) via secrets + IAM roles in AWS.
