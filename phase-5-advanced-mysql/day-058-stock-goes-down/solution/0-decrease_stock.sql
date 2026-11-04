-- A trigger, decrease_stock: after a new order goes in, take its number off the item's quantity.
-- Safe to run twice.
-- Write your statement below this line.
DROP TRIGGER IF EXISTS decrease_stock;
CREATE TRIGGER decrease_stock
AFTER INSERT ON orders
FOR EACH ROW
UPDATE items SET quantity = quantity - NEW.number WHERE name = NEW.item_name;
