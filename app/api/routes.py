"""API routes for estimator service."""

from __future__ import annotations

from fastapi import APIRouter, HTTPException

from app.estimator.engine import build_estimate
from app.estimator.schemas import EstimateInput, EstimateResult

router = APIRouter()


@router.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@router.post("/estimate", response_model=EstimateResult)
def estimate(payload: EstimateInput) -> EstimateResult:
    try:
        return build_estimate(payload)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
