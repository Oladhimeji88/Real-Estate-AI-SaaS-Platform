from fastapi import FastAPI

app = FastAPI(title="Search Service", version="0.1.0")

sample_listings = [
    {"listing_id": "l-1001", "title": "Modern 2BR downtown loft", "score": 0.91},
    {"listing_id": "l-1002", "title": "Family home near top schools", "score": 0.84},
    {"listing_id": "l-1003", "title": "Luxury condo with skyline views", "score": 0.8},
]

@app.get("/api/search")
def semantic_search(query: str):
    # TODO: replace with vector database search (pgvector/OpenSearch/Pinecone).
    return {"query": query, "results": sample_listings}

@app.get('/health')
def health():
    return {"status": "ok", "service": "search"}
