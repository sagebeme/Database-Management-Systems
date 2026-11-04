-- For each category: category and weekend_share, the percentage of its revenue earned on Saturdays and Sundays,
-- rounded to 1 decimal place. Highest share first, ties by category.
SELECT p.category,
       round(100.0 * sum(f.revenue) FILTER (WHERE d.is_weekend) / sum(f.revenue), 1) AS weekend_share
FROM fact_sales AS f
JOIN dim_date AS d ON d.date_key = f.date_key
JOIN dim_product AS p ON p.product_key = f.product_key
GROUP BY p.category
ORDER BY weekend_share DESC, p.category;
