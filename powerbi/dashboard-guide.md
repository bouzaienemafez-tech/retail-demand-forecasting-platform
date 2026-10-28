# Power BI Dashboard Blueprint

Connect Power BI to `data/warehouse/retail.db` after running ETL. Use `fact_sales` as the fact table and `dim_product` as the dimension table.

## Recommended page

- KPI cards: total revenue, units sold, average monthly demand.
- Line chart: units sold by sale month, split by product.
- Matrix: product, forecast demand, stock on hand, and inventory gap (from API output or an imported forecast table).
- Bar chart: revenue by category.
- Slicers: category and product name.

Frame the dashboard around a clear question: **Which products need replenishment next month?**
