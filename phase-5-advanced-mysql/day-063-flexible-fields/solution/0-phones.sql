-- Phones with at least 4 GB of RAM: name, ram_gb, storage_gb (as numbers), price. Cheapest first.
-- Write your statement below this line.
SELECT name,
       CAST(attributes->>'$.ram_gb' AS UNSIGNED) AS ram_gb,
       CAST(attributes->>'$.storage_gb' AS UNSIGNED) AS storage_gb,
       price
FROM products
WHERE category = 'phone' AND CAST(attributes->>'$.ram_gb' AS UNSIGNED) >= 4
ORDER BY price;
