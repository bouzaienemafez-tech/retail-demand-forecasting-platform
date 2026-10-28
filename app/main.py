from pathlib import Path
import joblib
import pandas as pd
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

ROOT = Path(__file__).resolve().parents[1]
MODEL = ROOT / "models/demand_forecaster.joblib"
app = FastAPI(title="Retail Demand Forecast API", version="1.0.0")


class ForecastRequest(BaseModel):
    product_id: str = Field(examples=["P-100"])
    month: int = Field(ge=1, le=12, examples=[11])
    trend: int = Field(ge=1, examples=[35], description="Sequential month number since the dataset start")
    stock_on_hand: int = Field(ge=0, examples=[40])


@app.get("/health")
def health():
    return {"status": "ready" if MODEL.exists() else "model_not_trained"}


@app.post("/forecast")
def forecast(request: ForecastRequest):
    if not MODEL.exists():
        raise HTTPException(status_code=503, detail="Model not trained. Run python src/etl.py then python src/train.py.")
    model = joblib.load(MODEL)
    forecast_units = max(0, round(float(model.predict(pd.DataFrame([request.model_dump(exclude={"stock_on_hand"})]))[0])))
    gap = forecast_units - request.stock_on_hand
    action = "Reorder immediately" if gap > 15 else "Plan replenishment" if gap > 0 else "Stock level is sufficient"
    return {"forecast_units": forecast_units, "stock_on_hand": request.stock_on_hand, "inventory_gap": gap, "recommendation": action}
