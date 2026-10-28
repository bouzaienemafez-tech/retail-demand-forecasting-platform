"""Generate retail sales and load an analytics-ready SQLite warehouse."""
import sqlite3
from datetime import date
from pathlib import Path
import random

ROOT = Path(__file__).resolve().parents[1]
DB = ROOT / "data/warehouse/retail.db"
PRODUCTS = [("P-100", "Wireless Headphones", "Electronics", 85.0), ("P-200", "Coffee Maker", "Home", 120.0), ("P-300", "Office Chair", "Furniture", 280.0)]


def month_dates():
    return [date(year, month, 1) for year in (2024, 2025) for month in range(1, 13)]


def load():
    random.seed(42)
    DB.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(DB)
    connection.executescript("""
    DROP TABLE IF EXISTS fact_sales;
    DROP TABLE IF EXISTS dim_product;
    CREATE TABLE dim_product (product_id TEXT PRIMARY KEY, product_name TEXT, category TEXT, unit_price REAL);
    CREATE TABLE fact_sales (sale_id INTEGER PRIMARY KEY, sale_month TEXT, product_id TEXT REFERENCES dim_product(product_id), units_sold INTEGER, revenue REAL);
    """)
    connection.executemany("INSERT INTO dim_product VALUES (?, ?, ?, ?)", PRODUCTS)
    sale_id = 1
    for index, month in enumerate(month_dates()):
        for product_id, _, _, price in PRODUCTS:
            seasonal = 18 if month.month in (11, 12) else 9 if month.month in (6, 7) else 0
            product_effect = {"P-100": 20, "P-200": 12, "P-300": 5}[product_id]
            trend = index * 1.5
            units = max(1, round(35 + seasonal + product_effect + trend + random.gauss(0, 5)))
            connection.execute("INSERT INTO fact_sales VALUES (?, ?, ?, ?, ?)", (sale_id, month.isoformat(), product_id, units, round(units * price, 2)))
            sale_id += 1
    connection.commit()
    rows = connection.execute("SELECT COUNT(*) FROM fact_sales").fetchone()[0]
    connection.close()
    print(f"Loaded {rows} sales records into {DB}")


if __name__ == "__main__":
    load()
