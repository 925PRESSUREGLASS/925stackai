# --- Similar Quotes Endpoint ---
from vector_store.quote_embedder import QuoteVectorStore
from fastapi import Body
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException, Body
from agents.quote_agent import run_quote
import json

app = FastAPI(title="Quote API")


class SimilarQuoteRequest(BaseModel):
    prompt: str
    top_k: int = 3


class SimilarQuoteMatch(BaseModel):
    content: str
    metadata: dict


class SimilarQuoteResponse(BaseModel):
    matches: list[SimilarQuoteMatch]


@app.post("/quote/similar", response_model=SimilarQuoteResponse)
def get_similar_quotes(request: SimilarQuoteRequest = Body(...)):
    vs = QuoteVectorStore()
    vs.build_index()
    matches = vs.query(request.prompt, top_k=request.top_k)
    return {"matches": matches}


class QuoteRequest(BaseModel):
    prompt: str


class QuoteResponse(BaseModel):
    customer: str
    items: list
    total: float
    memory_result: str | None = None


@app.post("/quote", response_model=QuoteResponse)
def get_quote(request: QuoteRequest):
    try:
        output = run_quote(request.prompt)
        data = json.loads(output)
        # Ensure memory_result is always present in response (None if missing)
        if "memory_result" not in data:
            data["memory_result"] = None
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
