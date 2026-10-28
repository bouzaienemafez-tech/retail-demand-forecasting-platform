import sqlite3
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from src.etl import DB, load


class WarehouseTests(unittest.TestCase):
    def test_etl_creates_expected_sales_grain(self):
        load()
        connection = sqlite3.connect(DB)
        self.assertEqual(connection.execute("SELECT COUNT(*) FROM fact_sales").fetchone()[0], 72)
        self.assertEqual(connection.execute("SELECT COUNT(DISTINCT product_id) FROM fact_sales").fetchone()[0], 3)
        connection.close()
