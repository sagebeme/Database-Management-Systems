-- A trigger, adjust_stock: when an order is changed, fix the stock. The number can change, and so can the
-- item (then the old item gets its number back and the new item loses the new number). Safe to run twice.
-- Write your statement below this line.
DROP TRIGGER IF EXISTS adjust_stock;
DELIMITER //
CREATE TRIGGER adjust_stock
AFTER UPDATE ON orders
FOR EACH ROW
BEGIN
    IF NEW.item_name = OLD.item_name THEN
        UPDATE items SET quantity = quantity - (NEW.number - OLD.number) WHERE name = NEW.item_name;
    ELSE
        UPDATE items SET quantity = quantity + OLD.number WHERE name = OLD.item_name;
        UPDATE items SET quantity = quantity - NEW.number WHERE name = NEW.item_name;
    END IF;
END //
DELIMITER ;
