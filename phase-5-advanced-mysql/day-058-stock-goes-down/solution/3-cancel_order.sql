-- A trigger, restore_stock: when an order is deleted (cancelled), put its number back. Safe to run twice.
-- Write your statement below this line.
DROP TRIGGER IF EXISTS restore_stock;
CREATE TRIGGER restore_stock
AFTER DELETE ON orders
FOR EACH ROW
UPDATE items SET quantity = quantity + OLD.number WHERE name = OLD.item_name;
