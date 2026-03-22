"""Tests for estimate orchestration, flags, and press selection behavior."""

import pytest

from engine import build_estimate
from schemas import EstimateInput


def _base_payload() -> dict:
    return {
        "customer_name": "Test Co",
        "inches_across": 2.0,
        "gap_across": 0.125,
        "inches_around": 3.0,
        "gap_around": 0.125,
        "shape": "rectangle",
        "facestock_spec": "Paper",
        "lam_spec": None,
        "printed": True,
        "total_colors": 4,
        "total_dies": 1,
        "qty_1": 1000,
        "qty_2": 5000,
        "qty_3": 10000,
        "target_margin_pct": 30.0,
        "labels_across": 1,
        "actual_web_width_in": None,
        "facestock_price_msi": 20.0,
        "lam_price_msi": None,
        "local_delivery_miles": 25.0,
    }


def test_valid_simple_printed_job() -> None:
    payload = EstimateInput(**_base_payload())
    result = build_estimate(payload)

    assert result.suggested_press == "Mark Andy 2200"
    assert len(result.qty_results) == 3
    assert result.qty_results[0].gross_margin_pct == 30.0


def test_contradiction_printed_false_with_colors_flagged() -> None:
    data = _base_payload()
    data["printed"] = False
    data["total_colors"] = 2

    result = build_estimate(EstimateInput(**data))

    assert "CONTRADICTION_PRINTED_FALSE_WITH_COLORS" in result.review_flags


def test_contradiction_printed_true_zero_colors_flagged() -> None:
    data = _base_payload()
    data["printed"] = True
    data["total_colors"] = 0

    result = build_estimate(EstimateInput(**data))

    assert "CONTRADICTION_PRINTED_TRUE_ZERO_COLORS" in result.review_flags


def test_out_of_scope_gt_8_colors_flagged_and_press_none() -> None:
    data = _base_payload()
    data["total_colors"] = 9

    result = build_estimate(EstimateInput(**data))

    assert "OUT_OF_SCOPE_COLORS_GT_8" in result.review_flags
    assert result.suggested_press is None


def test_missing_optional_pricing_fields_are_flagged() -> None:
    data = _base_payload()
    data["facestock_price_msi"] = None
    data["lam_spec"] = "matte varnish"
    data["lam_price_msi"] = None

    result = build_estimate(EstimateInput(**data))

    assert "MISSING_FACESTOCK_PRICE_MSI" in result.review_flags
    assert "MISSING_LAM_PRICE_MSI_FOR_LAMINATED_JOB" in result.review_flags


def test_invalid_dimensions_raise_value_error() -> None:
    data = _base_payload()
    data["inches_across"] = 0

    with pytest.raises(ValueError):
        build_estimate(EstimateInput(**data))
