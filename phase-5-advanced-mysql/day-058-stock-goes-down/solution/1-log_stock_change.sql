-- A trigger, log_stock_change: whenever an item's quantity changes, add a row to stock_log with the item's
-- name and its quantity before and after. Updates that don't change the quantity log nothing. Safe to run twice.
-- Write your statement below this line.
DROP TRIGGER IF EXISTS log_stock_change;
DELIMITER //
CREATE TRIGGER log_stock_change
AFTER UPDATE ON items
FOR EACH ROW
BEGIN
    IF NEW.quantity <> OLD.quantity THEN
        INSERT INTO stock_log (item_name, old_quantity, new_quantity) VALUES (NEW.name, OLD.quantity, NEW.quantity);
    END IF;
END //
DELIMITER ;
