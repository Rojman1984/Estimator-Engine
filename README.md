## Estimator-Engine (FastAPI POC)

Deterministic Python 3.11 FastAPI proof-of-concept estimator for narrow-web flexographic labels, designed to integrate with Monday.com workflows.

### What this includes

- Deterministic pricing engine (no LLM arithmetic in estimator core)
- Input/output contracts using Pydantic models
- Derived dimensions and 3-quantity estimate output
- Cost/label, sell price/label, gross profit, gross margin
- Simple press recommendation rules
- Review flags for contradictions and out-of-scope jobs
- Pytest test coverage for core pricing and orchestration

## Project structure

- `app/main.py` - FastAPI bootstrap
- `app/config.py` - environment configuration
- `app/api/routes.py` - API routes (`/health`, `/estimate`)
- `app/estimator/schemas.py` - Pydantic models
- `app/estimator/normalization.py` - normalization + review flags
- `app/estimator/pricing.py` - deterministic arithmetic core
- `app/estimator/press_selection.py` - press recommendation logic
- `app/estimator/engine.py` - orchestration for full estimate
- `tests/test_pricing.py` - unit tests for pricing math
- `tests/test_engine.py` - integration-style unit tests for engine behavior

## Assumptions used in pricing

- `material_overage_factor = 1.05`
- `blank_press_speed_ft_min = 350`
- `printed_press_speed_ft_min = 200`
- `blank_labor_rate_hr = 15.0`
- `printed_labor_rate_hr = 50.0`
- `overhead_rate_hr = 70.23`
- `base_setup_hours = 0.5`
- `hours_per_color = 0.1`
- `hours_per_die_after_first = 0.2`
- `lamination_setup_hours = 0.25`
- `admin_cost = 5.0`
- `other_cost = 25.0`
- `delivery_cost_per_mile = 0.5`

## API endpoints

- `GET /health` → `{"status": "ok"}`
- `POST /estimate` → deterministic estimate result

## Run locally (Windows PowerShell)

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Run tests:

```powershell
.\.venv\Scripts\Activate.ps1
pytest -q
```

## Example request body

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
  "target_margin_pct": 35.0,
  "labels_across": 2,
  "actual_web_width_in": null,
  "facestock_price_msi": 24.0,
  "lam_price_msi": 9.5,
  "local_delivery_miles": 20.0
}
```
