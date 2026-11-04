-- An index called idx_orders_customer, so that finding one customer's orders doesn't read the whole table.
CREATE INDEX idx_orders_customer ON orders (customer_id);
