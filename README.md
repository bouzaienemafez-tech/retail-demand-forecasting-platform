# Retail Demand Forecasting Platform

An end-to-end decision-intelligence platform for a retailer: it loads sales events, creates an analytics warehouse, forecasts next-month demand, and makes results available to both an API and a Power BI dashboard.

## Business problem

Retail teams must decide what to reorder before stockouts or excess inventory occur. This project predicts next-month unit demand for each product and translates the forecast into an inventory action.

## Architecture

```
Synthetic sales events → ETL validation → SQLite warehouse → ML training → Forecast API / Power BI
```

## Included components

- **ETL** — deterministic source generation, validation, deduplication and a fact/dimension warehouse.
- **SQL** — monthly product metrics and reorder-oriented analysis.
- **ML** — a trend-aware regression model using time and product signals.
- **API** — FastAPI endpoint that returns a demand forecast and inventory recommendation.
- **BI** — Power BI data model and dashboard blueprint.
- **Engineering** — Docker configuration and automated tests.

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python src/etl.py
python src/train.py
uvicorn app.main:app --reload
```

Then open `http://127.0.0.1:8000/docs` to test the forecast API.

## Recruiter talking points

This project demonstrates more than model training: it connects data quality, warehouse design, forecasting evaluation and a usable business interface. In an interview, discuss how you would replace the generated data with ERP/POS data, schedule the workflow with Airflow, track experiments with MLflow, and monitor forecast drift.

## Tech stack

`Python` · `SQLite` · `SQL` · `Pandas` · `scikit-learn` · `FastAPI` · `Power BI` · `Docker`
