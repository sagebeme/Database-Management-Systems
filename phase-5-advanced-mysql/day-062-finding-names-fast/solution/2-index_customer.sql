-- An index, idx_orders_customer, so looking up one customer's orders doesn't read the whole table.
-- Write your statement below this line.
CREATE INDEX idx_orders_customer ON orders (customer_id);
