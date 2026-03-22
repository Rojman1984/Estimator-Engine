"""Deterministic quantity-level pricing functions."""

from __future__ import annotations

from typing import Any

from schemas import QuantityEstimate

DEFAULT_ASSUMPTIONS: dict[str, float] = {
    "material_overage_factor": 1.05,
    "blank_press_speed_ft_min": 350,
    "printed_press_speed_ft_min": 200,
    "blank_labor_rate_hr": 15.0,
    "printed_labor_rate_hr": 50.0,
    "overhead_rate_hr": 70.23,
    "base_setup_hours": 0.5,
    "hours_per_color": 0.1,
    "hours_per_die_after_first": 0.2,
    "lamination_setup_hours": 0.25,
    "admin_cost": 5.0,
    "other_cost": 25.0,
    "delivery_cost_per_mile": 0.5,
}


def derive_values(normalized_input: dict[str, Any]) -> dict[str, float]:
    """Compute geometric derived values from normalized input."""

    effective_across = normalized_input["inches_across"] + normalized_input["gap_across"]
    effective_around = normalized_input["inches_around"] + normalized_input["gap_around"]
    face_area_sq_in = normalized_input["inches_across"] * normalized_input["inches_around"]
    pitch_area_sq_in = effective_across * effective_around
    per_label_msi = pitch_area_sq_in / 1000

    return {
        "effective_across": effective_across,
        "effective_around": effective_around,
        "face_area_sq_in": face_area_sq_in,
        "pitch_area_sq_in": pitch_area_sq_in,
        "per_label_msi": per_label_msi,
    }


def estimate_quantity(
    quantity: int,
    normalized_input: dict[str, Any],
    derived: dict[str, float],
    assumptions: dict[str, float] | None = None,
) -> QuantityEstimate:
    """Estimate one quantity with deterministic arithmetic."""

    cfg = assumptions or DEFAULT_ASSUMPTIONS
    laminated = bool(normalized_input["laminated"])

    press_speed = cfg["printed_press_speed_ft_min"] if normalized_input["printed"] else cfg["blank_press_speed_ft_min"]
    labor_rate = cfg["printed_labor_rate_hr"] if normalized_input["printed"] else cfg["blank_labor_rate_hr"]

    setup_hours = (
        cfg["base_setup_hours"]
        + normalized_input["total_colors"] * cfg["hours_per_color"]
        + max(normalized_input["total_dies"] - 1, 0) * cfg["hours_per_die_after_first"]
        + (cfg["lamination_setup_hours"] if laminated else 0.0)
    )

    run_length_ft = (((derived["effective_around"] * quantity) / normalized_input["labels_across"]) / 12)
    web_width = normalized_input["actual_web_width_in"]

    facestock_price_msi = normalized_input["facestock_price_msi"] or 0.0
    lam_price_msi = normalized_input["lam_price_msi"] if laminated and normalized_input["lam_price_msi"] else 0.0

    material_cost_total = (
        ((run_length_ft * web_width) / 1000)
        * (facestock_price_msi + lam_price_msi)
        * cfg["material_overage_factor"]
    )

    run_hours = (run_length_ft / press_speed) / 60
    total_hours = run_hours + setup_hours

    labor_total = total_hours * labor_rate
    overhead_total = total_hours * cfg["overhead_rate_hr"]
    delivery_total = normalized_input["local_delivery_miles"] * cfg["delivery_cost_per_mile"]

    total_cost = (
        material_cost_total
        + labor_total
        + overhead_total
        + cfg["admin_cost"]
        + cfg["other_cost"]
        + delivery_total
    )
    cost_per_label = total_cost / quantity

    sell_price_total = total_cost / (1 - (normalized_input["target_margin_pct"] / 100))
    sell_price_per_label = sell_price_total / quantity

    gross_profit = sell_price_total - total_cost
    gross_margin_pct = (gross_profit / sell_price_total) * 100

    return QuantityEstimate(
        quantity=quantity,
        total_cost=round(total_cost, 6),
        cost_per_label=round(cost_per_label, 6),
        sell_price_total=round(sell_price_total, 6),
        sell_price_per_label=round(sell_price_per_label, 6),
        gross_profit=round(gross_profit, 6),
        gross_margin_pct=round(gross_margin_pct, 6),
    )
