"""Pydantic schemas for the deterministic estimator POC."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class EstimateInput(BaseModel):
    """Input payload coming from Monday.com for a single estimator item."""

    customer_name: str
    inches_across: float
    gap_across: float
    inches_around: float
    gap_around: float
    shape: str | None = None
    facestock_spec: str | None = None
    lam_spec: str | None = None
    printed: bool
    total_colors: int
    total_dies: int
    qty_1: int
    qty_2: int
    qty_3: int
    target_margin_pct: float
    labels_across: int | None = 1
    actual_web_width_in: float | None = None
    facestock_price_msi: float | None = None
    lam_price_msi: float | None = None
    local_delivery_miles: float | None = 0


class QuantityEstimate(BaseModel):
    """Cost and sell-side results for one requested quantity."""

    quantity: int
    total_cost: float
    cost_per_label: float
    sell_price_total: float
    sell_price_per_label: float
    gross_profit: float
    gross_margin_pct: float


class EstimateResult(BaseModel):
    """Full normalized estimate result returned to Monday.com and summarizers."""

    normalized_input: dict[str, Any]
    derived_values: dict[str, Any]
    complexity_score: float
    suggested_press: str | None
    review_flags: list[str] = Field(default_factory=list)
    assumptions_used: dict[str, Any]
    qty_results: list[QuantityEstimate]
    total_cost_per_unit_reference: float | None = None
