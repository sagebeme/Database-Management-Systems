-- The three items that sold the most units: item and units, most first, ties alphabetical.
SELECT item, SUM(qty) AS units FROM sales GROUP BY item ORDER BY units DESC, item LIMIT 3;
