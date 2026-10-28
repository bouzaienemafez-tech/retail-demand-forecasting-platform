-- Product demand and revenue trend for dashboard use
SELECT f.sale_month, p.product_name, p.category,
       f.units_sold, f.revenue,
       AVG(f.units_sold) OVER (PARTITION BY f.product_id ORDER BY f.sale_month ROWS BETWEEN 2 PRECEDING AND CURRENT ROW) AS rolling_3_month_demand
FROM fact_sales f
JOIN dim_product p ON p.product_id = f.product_id
ORDER BY f.sale_month, p.product_name;
