# Retail Demand Forecasting Platform

A runnable **synthetic-data portfolio demo** connecting Python data generation, a SQLite fact/dimension model, SQL analytics, Ridge regression and a FastAPI inventory interface.

**Business question:** how can monthly product demand estimates support replenishment decisions? The API compares a forecast with supplied stock; its recommendations are illustrative rules, not an optimized inventory policy.

## What is implemented

| Component | Evidence and scope |
| --- | --- |
| Data generation and loading | [src/etl.py](src/etl.py): seed 42; 72 product-month observations, 3 products, January 2024–December 2025; recreates SQLite tables on every run |
| Analytics warehouse | `dim_product` and `fact_sales` in `data/warehouse/retail.db` |
| SQL analysis | [sql/analytics.sql](sql/analytics.sql): product/category revenue and a trailing three-month demand average |
| Forecasting | [src/train.py](src/train.py): one-hot product/month features, numeric time trend and Ridge regression |
| API | [app/main.py](app/main.py): health check, forecast and stock-gap recommendation |
| Test | [tests/test_etl.py](tests/test_etl.py): checks 72 rows and 3 distinct products |
| Container definition | [Dockerfile](Dockerfile): generates data and trains during image build; container execution remains unverified |
| Power BI | [Dashboard blueprint](powerbi/dashboard-guide.md) only; no completed report, screenshot or forecast export is included |

```text
Seeded synthetic product-month data → SQLite → Ridge model → FastAPI
                                        └→ SQL analytics → planned Power BI report
```

## Run locally

Verified with Python 3.13.7 on macOS ARM64. The Dockerfile specifies Python 3.12.
Run commands from the repository root. No dataset download or credentials are needed.

```bash
git clone https://github.com/bouzaienemafez-tech/retail-demand-forecasting-platform.git
cd retail-demand-forecasting-platform
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python src/etl.py
python src/train.py
python -m unittest discover -s tests -v
python -m uvicorn app.main:app --reload
```

Windows PowerShell activation: `.venv\Scripts\Activate.ps1`.
Open http://127.0.0.1:8000/docs for the interactive API.

ETL **drops and recreates** the two demo tables. The generated database and model are ignored by Git. Training must precede inference; the service returns HTTP 503 when the model is absent. `/health` checks file existence, not full model readiness.

### Example request

January 2026 is month 1 and trend 25 because January 2024 is trend 1.
The saved model is fitted through October 2025; it is not refitted on the holdout.

```bash
curl -X POST http://127.0.0.1:8000/forecast \
  -H 'Content-Type: application/json' \
  -d '{"product_id":"P-100","month":1,"trend":25,"stock_on_hand":40}'
```

Observed response in the verified environment:

```json
{"forecast_units":92,"stock_on_hand":40,"inventory_gap":52,"recommendation":"Reorder immediately"}
```

Use known products `P-100`, `P-200`, `P-300`. The API does not reject unknown product IDs or check consistency between month and trend.

## Results and interpretation

| Measure | Observed result |
| --- | --- |
| Training set | 66 product-month rows, January 2024–October 2025 |
| Holdout | 6 rows, November–December 2025 across 3 products |
| Holdout MAE | **8.39 units** |
| Existing automated tests | 1 passed |

These are results on generated data, not measured retail performance. The six-row holdout is small, covers only two months and has no naïve baseline comparison. It does not establish forecast reliability, stockout reduction or financial impact. See [verification details](docs/verification.md) for provenance and checks.

## Limits and next steps

- The loader generates clean data; external-source validation and deduplication are not implemented.
- Add seasonal-naïve baselines and rolling-origin evaluation before claiming forecasting improvement.
- Add real-data ingestion, stronger data-quality tests and calendar/product validation.
- Build and validate the Power BI report, with a forecast export and genuine screenshots.
- Scheduling, experiment tracking, monitoring, authentication and production deployment are future work.

**Skills demonstrated:** Python, Pandas, SQLite/SQL, dimensional modeling, regression, temporal holdout evaluation and FastAPI. Power BI is currently a design exercise.
