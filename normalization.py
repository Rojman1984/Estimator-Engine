"""Input normalization and validation utilities for estimator jobs."""

from __future__ import annotations

import math
from typing import Any

from schemas import EstimateInput


def _reasonable_web_width(effective_across: float) -> float:
    """Round fallback web width up to the nearest 0.5 inch, minimum 1.0 inch."""

    return max(1.0, math.ceil(effective_across * 2) / 2)


def normalize_input(payload: EstimateInput) -> tuple[dict[str, Any], list[str]]:
    """Normalize payload into a plain dictionary and collect non-fatal flags."""

    normalized = payload.model_dump()
    flags: list[str] = []

    for field in ("inches_across", "gap_across", "inches_around", "gap_around"):
        value = float(normalized[field])
        if value <= 0:
            raise ValueError(f"{field} must be greater than 0")

    if normalized["total_dies"] < 1:
        raise ValueError("total_dies must be >= 1")

    if normalized["labels_across"] is None:
        normalized["labels_across"] = 1
    if normalized["labels_across"] < 1:
        raise ValueError("labels_across must be >= 1")

    for qty_field in ("qty_1", "qty_2", "qty_3"):
        if int(normalized[qty_field]) <= 0:
            raise ValueError(f"{qty_field} must be greater than 0")

    target_margin_pct = float(normalized["target_margin_pct"])
    if not 0 <= target_margin_pct < 100:
        raise ValueError("target_margin_pct must be >= 0 and < 100")

    total_colors = int(normalized["total_colors"])
    if total_colors < 0:
        raise ValueError("total_colors must be >= 0")
    if total_colors > 8:
        flags.append("OUT_OF_SCOPE_COLORS_GT_8")

    printed = bool(normalized["printed"])
    if not printed and total_colors > 0:
        flags.append("CONTRADICTION_PRINTED_FALSE_WITH_COLORS")
    if printed and total_colors == 0:
        flags.append("CONTRADICTION_PRINTED_TRUE_ZERO_COLORS")

    laminated = bool(normalized.get("lam_spec"))
    normalized["laminated"] = laminated

    if normalized.get("actual_web_width_in") is None:
        effective_across = normalized["inches_across"] + normalized["gap_across"]
        normalized["actual_web_width_in"] = _reasonable_web_width(effective_across)
        flags.append("USING_DERIVED_WEB_WIDTH")

    if normalized.get("facestock_price_msi") is None:
        flags.append("MISSING_FACESTOCK_PRICE_MSI")
    if laminated and normalized.get("lam_price_msi") is None:
        flags.append("MISSING_LAM_PRICE_MSI_FOR_LAMINATED_JOB")

    if normalized.get("local_delivery_miles") is None:
        normalized["local_delivery_miles"] = 0.0

    return normalized, flags
