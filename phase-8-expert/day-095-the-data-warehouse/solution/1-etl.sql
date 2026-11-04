-- Load the warehouse from the shop system (extract, transform, load):
--   dim_date: one row for every day from 2026-01-01 to 2026-12-31;
--   dim_shop: every shop, valid from 2026-01-01, current; dim_product: every product;
--   fact_sales: one row per sale, with revenue = qty * the product's price, pointing at the right dimension rows.
INSERT INTO dim_date
SELECT to_char(d, 'YYYYMMDD')::int, d, extract(month FROM d), extract(quarter FROM d), extract(year FROM d),
       trim(to_char(d, 'Day')), extract(isodow FROM d) >= 6
FROM generate_series(DATE '2026-01-01', DATE '2026-12-31', INTERVAL '1 day') AS g(d);
INSERT INTO dim_shop (shop_id, name, county, valid_from, valid_to, is_current)
SELECT id, name, county, DATE '2026-01-01', NULL, true FROM shops;
INSERT INTO dim_product (product_id, name, category)
SELECT id, name, category FROM products;
INSERT INTO fact_sales (date_key, shop_key, product_key, qty, revenue)
SELECT to_char(s.sold_at, 'YYYYMMDD')::int, ds.shop_key, dp.product_key, s.qty, s.qty * p.price
FROM sales AS s
JOIN products AS p ON p.id = s.product_id
JOIN dim_shop AS ds ON ds.shop_id = s.shop_id AND ds.is_current
JOIN dim_product AS dp ON dp.product_id = s.product_id;
