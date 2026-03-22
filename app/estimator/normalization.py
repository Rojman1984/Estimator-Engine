"""Normalization and review-flag helpers."""

from __future__ import annotations

import math
from typing import Any

from app.estimator.schemas import EstimateInput


def _derive_web_width(effective_across: float, labels_across: int) -> float:
    raw_width = effective_across * labels_across
    return max(1.0, math.ceil(raw_width * 2) / 2)


def normalize_input(payload: EstimateInput) -> tuple[dict[str, Any], list[str]]:
    normalized = payload.model_dump()
    flags: list[str] = []

    normalized["labels_across"] = normalized.get("labels_across") or 1
    normalized["local_delivery_miles"] = normalized.get("local_delivery_miles") or 0.0

    laminated = bool((normalized.get("lam_spec") or "").strip())
    normalized["laminated"] = laminated

    printed = bool(normalized["printed"])
    total_colors = int(normalized["total_colors"])

    if not printed and total_colors > 0:
        flags.append("CONTRADICTION_PRINTED_FALSE_WITH_COLORS")
    if printed and total_colors == 0:
        flags.append("CONTRADICTION_PRINTED_TRUE_ZERO_COLORS")
    if total_colors > 8:
        flags.append("OUT_OF_SCOPE_COLORS_GT_8")

    effective_across = float(normalized["inches_across"]) + float(normalized["gap_across"])
    if normalized.get("actual_web_width_in") is None:
        normalized["actual_web_width_in"] = _derive_web_width(effective_across, int(normalized["labels_across"]))
        flags.append("USING_DERIVED_WEB_WIDTH")

    if normalized.get("facestock_price_msi") is None:
        flags.append("MISSING_FACESTOCK_PRICE_MSI")

    if laminated and normalized.get("lam_price_msi") is None:
        flags.append("MISSING_LAM_PRICE_MSI_FOR_LAMINATED_JOB")

    if (not laminated) and normalized.get("lam_price_msi") is not None:
        flags.append("LAM_PRICE_PROVIDED_FOR_NON_LAMINATED_JOB")

    return normalized, flags
