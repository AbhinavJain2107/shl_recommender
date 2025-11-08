from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from src.recommender import recommend

app = FastAPI(title="SHL Assessment Recommender")

class RecommendRequest(BaseModel):
    query: str
    top_k: int = 5

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.post("/recommend")
def recommend_api(req: RecommendRequest):
    if not req.query.strip():
        raise HTTPException(status_code=400, detail="Empty query")
    results = recommend(req.query, top_k=req.top_k)
    return {"query": req.query, "results": results}
@app.get("/")
def home():
    return {"message": "Welcome to the SHL Assessment Recommender API! Visit /docs to use it."}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
