"""Pydantic schemas for estimator API."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field, field_validator, model_validator


class EstimateInput(BaseModel):
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

    @field_validator("customer_name")
    @classmethod
    def customer_name_not_blank(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("customer_name must not be blank")
        return value.strip()

    @field_validator("inches_across", "gap_across", "inches_around", "gap_around")
    @classmethod
    def dimensions_positive(cls, value: float) -> float:
        if value <= 0:
            raise ValueError("dimensions and gaps must be greater than 0")
        return value

    @field_validator("total_colors")
    @classmethod
    def colors_non_negative(cls, value: int) -> int:
        if value < 0:
            raise ValueError("total_colors must be >= 0")
        return value

    @field_validator("total_dies")
    @classmethod
    def dies_positive(cls, value: int) -> int:
        if value < 1:
            raise ValueError("total_dies must be >= 1")
        return value

    @field_validator("qty_1", "qty_2", "qty_3")
    @classmethod
    def qty_positive(cls, value: int) -> int:
        if value <= 0:
            raise ValueError("quantities must be greater than 0")
        return value

    @field_validator("target_margin_pct")
    @classmethod
    def margin_range(cls, value: float) -> float:
        if not 0 <= value < 100:
            raise ValueError("target_margin_pct must be >= 0 and < 100")
        return value

    @field_validator("labels_across")
    @classmethod
    def labels_across_valid(cls, value: int | None) -> int:
        resolved = 1 if value is None else value
        if resolved < 1:
            raise ValueError("labels_across must be >= 1")
        return resolved

    @field_validator("actual_web_width_in")
    @classmethod
    def web_width_positive_when_present(cls, value: float | None) -> float | None:
        if value is not None and value <= 0:
            raise ValueError("actual_web_width_in must be > 0 when provided")
        return value

    @field_validator("facestock_price_msi", "lam_price_msi")
    @classmethod
    def prices_non_negative_when_present(cls, value: float | None) -> float | None:
        if value is not None and value < 0:
            raise ValueError("price MSI values must be >= 0")
        return value

    @field_validator("local_delivery_miles")
    @classmethod
    def miles_non_negative(cls, value: float | None) -> float:
        resolved = 0.0 if value is None else value
        if resolved < 0:
            raise ValueError("local_delivery_miles must be >= 0")
        return resolved

    @model_validator(mode="after")
    def validate_qty_order(self) -> "EstimateInput":
        if not (self.qty_1 <= self.qty_2 <= self.qty_3):
            raise ValueError("Quantities must be ascending: qty_1 <= qty_2 <= qty_3")
        return self


class QuantityEstimate(BaseModel):
    quantity: int
    total_cost: float
    cost_per_label: float
    sell_price_total: float
    sell_price_per_label: float
    gross_profit: float
    gross_margin_pct: float


class EstimateResult(BaseModel):
    normalized_input: dict[str, Any]
    derived_values: dict[str, Any]
    complexity_score: float
    suggested_press: str | None
    review_flags: list[str] = Field(default_factory=list)
    assumptions_used: dict[str, float]
    qty_results: list[QuantityEstimate]
    total_cost_per_unit_reference: float | None = None
