"""Tests for deterministic pricing functions."""

from app.estimator.pricing import DEFAULT_ASSUMPTIONS, derive_values, estimate_quantity


def test_blank_label_zero_colors_uses_blank_rates() -> None:
    normalized = {
        "customer_name": "Acme",
        "inches_across": 2.0,
        "gap_across": 0.125,
        "inches_around": 3.0,
        "gap_around": 0.125,
        "shape": None,
        "facestock_spec": None,
        "lam_spec": None,
        "laminated": False,
        "printed": False,
        "total_colors": 0,
        "total_dies": 1,
        "qty_1": 1000,
        "qty_2": 5000,
        "qty_3": 10000,
        "target_margin_pct": 30.0,
        "labels_across": 1,
        "actual_web_width_in": 2.5,
        "facestock_price_msi": 20.0,
        "lam_price_msi": None,
        "local_delivery_miles": 10.0,
    }
    derived = derive_values(normalized)

    result = estimate_quantity(1000, normalized, derived, DEFAULT_ASSUMPTIONS)

    assert result.quantity == 1000
    assert result.total_cost > 0
    assert result.gross_margin_pct == 30.0


def test_laminated_7_color_job_costs_are_calculated() -> None:
    normalized = {
        "customer_name": "Brand X",
        "inches_across": 2.5,
        "gap_across": 0.125,
        "inches_around": 4.0,
        "gap_around": 0.125,
        "shape": "oval",
        "facestock_spec": "PP",
        "lam_spec": "Gloss lam",
        "laminated": True,
        "printed": True,
        "total_colors": 7,
        "total_dies": 2,
        "qty_1": 5000,
        "qty_2": 10000,
        "qty_3": 25000,
        "target_margin_pct": 35.0,
        "labels_across": 2,
        "actual_web_width_in": 5.0,
        "facestock_price_msi": 25.0,
        "lam_price_msi": 10.0,
        "local_delivery_miles": 0.0,
    }
    derived = derive_values(normalized)

    result = estimate_quantity(10000, normalized, derived, DEFAULT_ASSUMPTIONS)

    assert result.total_cost > 0
    assert result.sell_price_total > result.total_cost
    assert result.gross_margin_pct == 35.0
