# --- Similar Quotes Endpoint ---
import json

"""FastAPI application exposing the quoting endpoints."""

from __future__ import annotations

import argparse
import uvicorn
from fastapi import Body, FastAPI, HTTPException
from pydantic import BaseModel

from agents.quote_agent import run_quote
from vector_store.quote_embedder import QuoteVectorStore

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


def main() -> None:
    """CLI entrypoint to run the API with ``uvicorn``."""
    parser = argparse.ArgumentParser(description="Run the Quote API server")
    parser.add_argument("--host", default="0.0.0.0")
    parser.add_argument("--port", type=int, default=8000)
    parser.add_argument("--reload", action="store_true", help="Enable reload")
    args = parser.parse_args()
    uvicorn.run("app_quote_api:app", host=args.host, port=args.port, reload=args.reload)


if __name__ == "__main__":
    main()
