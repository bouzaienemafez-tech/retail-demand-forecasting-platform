# Verification record

Verified locally on 2026-11-05 using Python 3.13.7 on macOS ARM64.
Source commit: `e8dd11349b24ac88b947de92da77bd93303518dc`. This documentation change does not alter model or API code.

## Reproduce

Follow the README setup from the repository root. [verified-environment.txt](verified-environment.txt) records all installed package versions, including HTTPX used for verification. It is an environment snapshot, not a cross-platform lockfile. Direct dependencies are pinned in requirements.txt; transitive dependencies otherwise resolve at installation time.

Commands executed:
```bash
python src/etl.py
python src/train.py
python -m unittest discover -s tests -v
```

Observed: 72 sales records, holdout MAE 8.39 units, 1 test passed.
Training uses 66 rows; the six most recent rows form the November–December 2025 holdout.
The saved model is the training-split model, not a refit on all 72 rows.
The ETL test checks row and product counts; it does not test deduplication, data validation or forecasting quality.

## API checks performed

Using FastAPI TestClient and HTTPX 0.28.1 against the trained model:
- GET /health returned ready.
- The README example returned HTTP 200 and the displayed JSON response.
- A negative month returned HTTP 422.
- With the model path temporarily pointed to an absent file, health returned model_not_trained and inference returned HTTP 503.

These were local smoke checks, not a full test suite or a deployed-network check.

## Not verified

Docker build/run, Windows setup, Python 3.12 execution, hosted deployment, real-data performance, business impact, and a Power BI report.
No screenshots are supplied because no finished dashboard or deployed application was verified.
