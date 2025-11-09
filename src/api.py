from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.responses import JSONResponse
from src.recommender import recommend


# Request model for Swagger UI
class QueryRequest(BaseModel):
    query: str


app = FastAPI(
    title="SHL Assessment Recommendation API",
    description="Recommends relevant SHL assessments based on job description or query text.",
    version="1.0.0"
)


@app.get("/health")
def health():
    """Health check endpoint"""
    return {"status": "ok"}


@app.post("/recommend")
def recommend_assessment(payload: QueryRequest):
    """
    Accepts a job description or natural language query and returns recommended SHL assessments.
    """
    try:
        query = payload.query
        recs = recommend(query, top_k=10)

        formatted = []
        for r in recs:
            formatted.append({
                "url": r.get("url", ""),
                "name": r.get("assessment_name", "Unknown Assessment"),
                "adaptive_support": "Yes",
                "description": "Relevant SHL assessment based on query context.",
                "duration": 60,
                "remote_support": "Yes",
                "test_type": ["Knowledge & Skills"]
            })

        return {"recommended_assessments": formatted}

    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": f"Internal server error: {str(e)}"}
        )