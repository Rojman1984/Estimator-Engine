"""Estimator orchestration entrypoint."""

from __future__ import annotations

from app.estimator.normalization import normalize_input
from app.estimator.press_selection import complexity_score, suggest_press
from app.estimator.pricing import DEFAULT_ASSUMPTIONS, derive_values, estimate_quantity
from app.estimator.schemas import EstimateInput, EstimateResult


def build_estimate(payload: EstimateInput) -> EstimateResult:
    normalized_input, flags = normalize_input(payload)
    derived = derive_values(normalized_input)

    press, press_flags = suggest_press(
        total_colors=normalized_input["total_colors"],
        laminated=normalized_input["laminated"],
        total_dies=normalized_input["total_dies"],
    )
    flags.extend(press_flags)

    qty_results = [
        estimate_quantity(normalized_input["qty_1"], normalized_input, derived, DEFAULT_ASSUMPTIONS),
        estimate_quantity(normalized_input["qty_2"], normalized_input, derived, DEFAULT_ASSUMPTIONS),
        estimate_quantity(normalized_input["qty_3"], normalized_input, derived, DEFAULT_ASSUMPTIONS),
    ]

    return EstimateResult(
        normalized_input=normalized_input,
        derived_values=derived,
        complexity_score=complexity_score(
            printed=normalized_input["printed"],
            total_colors=normalized_input["total_colors"],
            laminated=normalized_input["laminated"],
            total_dies=normalized_input["total_dies"],
            shape=normalized_input.get("shape"),
        ),
        suggested_press=press,
        review_flags=sorted(set(flags)),
        assumptions_used=DEFAULT_ASSUMPTIONS,
        qty_results=qty_results,
        total_cost_per_unit_reference=qty_results[-1].cost_per_label,
    )
