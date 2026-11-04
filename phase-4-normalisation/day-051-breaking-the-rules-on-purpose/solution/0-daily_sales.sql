-- A summary table: daily_sales (shop_id, day, order_count, revenue), primary key (shop_id, day), one row for
-- each shop and day that has orders. Create it and fill it from orders.
-- Write your statement below this line.
DROP TABLE IF EXISTS daily_sales;
CREATE TABLE daily_sales (
    shop_id INT NOT NULL,
    day DATE NOT NULL,
    order_count INT NOT NULL,
    revenue INT NOT NULL,
    PRIMARY KEY (shop_id, day)
);
INSERT INTO daily_sales
SELECT shop_id, placed_on, COUNT(*), SUM(total) FROM orders GROUP BY shop_id, placed_on;
