# Power BI Dashboard Blueprint

This is a proposed report design, not an implemented Power BI dashboard. No `.pbix` file, screenshots, SQLite connection setup or forecast export is included.

After running ETL, `data/warehouse/retail.db` contains `fact_sales` and `dim_product`. A future report should import these tables using a separately configured SQLite connection or CSV export, then relate `dim_product.product_id` (one) to `fact_sales.product_id` (many). Neither ingestion route has been verified in Power BI.

## Recommended page

- KPI cards: total revenue, units sold, average monthly demand.
- Line chart: units sold by sale month, split by product.
- Matrix: product, forecast demand, stock on hand, and inventory gap (from API output or an imported forecast table).
- Bar chart: revenue by category.
- Slicers: category and product name.

Frame the dashboard around a clear question: **Which products need replenishment next month?**

The current warehouse contains historical synthetic observations only. To implement the forecast matrix, first add an export containing product ID, target month, predicted units, stock on hand and inventory gap. Stock levels are API inputs, not warehouse data. Validate the report against SQL totals before adding genuine screenshots to the README.
