-- For every town that has shops: town_id, and the name and monthly_sales of its best-selling shop. In town_id order.
SELECT town_id, name, monthly_sales
FROM shops AS s
WHERE monthly_sales = (SELECT MAX(monthly_sales) FROM shops WHERE town_id = s.town_id)
ORDER BY town_id;
