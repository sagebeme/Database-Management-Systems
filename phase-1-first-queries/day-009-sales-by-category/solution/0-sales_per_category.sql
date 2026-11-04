-- Each category and its number of sales (sales), most sales first, ties alphabetical.
SELECT category, COUNT(*) AS sales FROM sales GROUP BY category ORDER BY sales DESC, category;
