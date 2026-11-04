-- Every tag and how many products carry it: tag, products. Most first, ties by tag.
-- Write your statement below this line.
SELECT t.tag, COUNT(*) AS products
FROM products AS p,
     JSON_TABLE(p.attributes, '$.tags[*]' COLUMNS (tag VARCHAR(30) PATH '$')) AS t
GROUP BY t.tag
ORDER BY products DESC, t.tag;
