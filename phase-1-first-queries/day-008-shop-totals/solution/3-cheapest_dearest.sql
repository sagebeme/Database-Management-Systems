-- The lowest and highest unit price sold, in columns cheapest and dearest.
SELECT MIN(unit_price) AS cheapest, MAX(unit_price) AS dearest FROM sales;
