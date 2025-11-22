"""
FastAPI endpoint for the AI Hallucination Meter.
Useful for Chrome extension or API integration.
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import os
from core.hallucination_meter import HallucinationMeter


app = FastAPI(
    title="TruthLens AI API",
    description="API for evaluating LLM output for hallucinations",
    version="1.0.0"
)

# Enable CORS for Chrome extension
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class TextEvaluationRequest(BaseModel):
    """Request model for text evaluation."""
    text: str
    llm_provider: Optional[str] = "openai"
    retrieval_method: Optional[str] = "wikipedia"
    use_llm_verification: Optional[bool] = True


class QueryEvaluationRequest(BaseModel):
    """Request model for query evaluation."""
    query: str
    llm_provider: Optional[str] = "openai"
    retrieval_method: Optional[str] = "wikipedia"
    use_llm_verification: Optional[bool] = True


@app.get("/")
def root():
    """Root endpoint."""
    return {
        "message": "TruthLens AI API",
        "version": "1.0.0",
        "endpoints": {
            "/check": "POST - Evaluate text for hallucinations",
            "/query": "POST - Generate answer and evaluate",
            "/health": "GET - Health check"
        }
    }


@app.get("/health")
def health():
    """Health check endpoint."""
    return {"status": "healthy"}


@app.post("/check")
def check_hallucination(request: TextEvaluationRequest):
    """
    Evaluate text for hallucinations.
    
    Example:
    ```json
    {
        "text": "Beethoven met Mozart in Vienna in 1787.",
        "llm_provider": "openai",
        "retrieval_method": "wikipedia",
        "use_llm_verification": true
    }
    ```
    """
    try:
        meter = HallucinationMeter(
            llm_provider=request.llm_provider,
            retrieval_method=request.retrieval_method,
            use_llm_verification=request.use_llm_verification
        )
        
        result = meter.evaluate(request.text)
        
        return {
            "success": True,
            "result": result
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/query")
def query_and_evaluate(request: QueryEvaluationRequest):
    """
    Generate answer to query and evaluate it.
    
    Example:
    ```json
    {
        "query": "Did Beethoven meet Mozart?",
        "llm_provider": "openai",
        "retrieval_method": "wikipedia",
        "use_llm_verification": true
    }
    ```
    """
    try:
        meter = HallucinationMeter(
            llm_provider=request.llm_provider,
            retrieval_method=request.retrieval_method,
            use_llm_verification=request.use_llm_verification
        )
        
        result = meter.evaluate_query(request.query)
        
        return {
            "success": True,
            "result": result
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

