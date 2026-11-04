-- Revenue by county and category, with a subtotal for each county and a grand total, in one query with ROLLUP:
-- county, category, revenue. Subtotal rows have category NULL; the grand total has both NULL. Ordered by county
-- then category, NULLs (the totals) after the rest.
SELECT s.county, p.category, sum(f.revenue) AS revenue
FROM fact_sales AS f
JOIN dim_shop AS s ON s.shop_key = f.shop_key
JOIN dim_product AS p ON p.product_key = f.product_key
GROUP BY ROLLUP (s.county, p.category)
ORDER BY s.county NULLS LAST, p.category NULLS LAST;
