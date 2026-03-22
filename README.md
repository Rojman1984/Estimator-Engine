## Estimator Workspace POC (Python)

Deterministic narrow-web flexographic pressure-sensitive label estimator for Monday.com board items.

### Run locally

1. Create and activate a Python 3.11+ virtual environment.
2. Install dependencies:

```bash
pip install fastapi uvicorn pydantic pytest
```

3. Run API:

```bash
uvicorn main:app --reload
```

4. Run tests:

```bash
pytest -q
```

### API

- `GET /health` returns `{"status": "ok"}`
- `POST /estimate` accepts `EstimateInput` and returns `EstimateResult`

### Example request JSON (`POST /estimate`)

```json
{
  "customer_name": "Acme Labels",
  "inches_across": 2.0,
  "gap_across": 0.125,
  "inches_around": 3.0,
  "gap_around": 0.125,
  "shape": "oval",
  "facestock_spec": "BOPP White",
  "lam_spec": "Gloss Lam",
  "printed": true,
  "total_colors": 6,
  "total_dies": 2,
  "qty_1": 1000,
  "qty_2": 5000,
  "qty_3": 10000,
  "target_margin_pct": 35,
  "labels_across": 2,
  "actual_web_width_in": null,
  "facestock_price_msi": 24.0,
  "lam_price_msi": 9.5,
  "local_delivery_miles": 20
}
```

### Example response JSON (truncated)

```json
{
  "normalized_input": {
    "customer_name": "Acme Labels",
    "laminated": true
  },
  "derived_values": {
    "effective_across": 2.125,
    "effective_around": 3.125,
    "per_label_msi": 0.006640625
  },
  "complexity_score": 8.0,
  "suggested_press": "Mark Andy 4200",
  "review_flags": [
    "USING_DERIVED_WEB_WIDTH"
  ],
  "assumptions_used": {
    "material_overage_factor": 1.05
  },
  "qty_results": [
    {
      "quantity": 1000,
      "total_cost": 180.0,
      "cost_per_label": 0.18,
      "sell_price_total": 276.923077,
      "sell_price_per_label": 0.276923,
      "gross_profit": 96.923077,
      "gross_margin_pct": 35.0
    }
  ],
  "total_cost_per_unit_reference": 0.12
}
```
