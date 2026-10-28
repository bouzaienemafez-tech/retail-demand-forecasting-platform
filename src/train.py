"""Train a product-level demand forecast model from the warehouse."""
from pathlib import Path
import sqlite3
import joblib
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_absolute_error
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder

ROOT = Path(__file__).resolve().parents[1]
DB = ROOT / "data/warehouse/retail.db"
MODEL = ROOT / "models/demand_forecaster.joblib"


def train():
    query = "SELECT sale_month, product_id, units_sold FROM fact_sales ORDER BY sale_month"
    data = pd.read_sql_query(query, sqlite3.connect(DB))
    data["date"] = pd.to_datetime(data["sale_month"])
    data["month"] = data["date"].dt.month
    data["trend"] = (data["date"].dt.year - data["date"].dt.year.min()) * 12 + data["month"]
    train_data, test_data = data.iloc[:-6], data.iloc[-6:]
    transform = ColumnTransformer([("seasonal_product", OneHotEncoder(handle_unknown="ignore"), ["product_id", "month"])], remainder="passthrough")
    model = Pipeline([("features", transform), ("forecast", Ridge(alpha=1.0))])
    features = ["product_id", "month", "trend"]
    model.fit(train_data[features], train_data["units_sold"])
    predictions = model.predict(test_data[features])
    print(f"Holdout MAE: {mean_absolute_error(test_data['units_sold'], predictions):.2f} units")
    MODEL.parent.mkdir(exist_ok=True)
    joblib.dump(model, MODEL)
    print(f"Saved model to {MODEL}")


if __name__ == "__main__":
    train()
