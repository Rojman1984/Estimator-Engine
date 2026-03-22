"""FastAPI application entrypoint for estimator engine."""

from __future__ import annotations

from fastapi import FastAPI, HTTPException

from engine import build_estimate
from schemas import EstimateInput, EstimateResult

app = FastAPI(title="Estimator Workspace API", version="0.1.0")


@app.get("/health")
def health() -> dict[str, str]:
    """Health endpoint for liveness checks."""

    return {"status": "ok"}


@app.post("/estimate", response_model=EstimateResult)
def estimate(payload: EstimateInput) -> EstimateResult:
    """Run deterministic estimate logic and return structured output."""

    try:
        return build_estimate(payload)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
