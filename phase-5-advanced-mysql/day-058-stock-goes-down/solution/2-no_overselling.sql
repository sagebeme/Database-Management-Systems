-- A trigger, no_overselling: refuse an order for more than is in stock, with SQLSTATE '45000' and the message
-- 'Not enough stock'. Safe to run twice.
-- Write your statement below this line.
DROP TRIGGER IF EXISTS no_overselling;
DELIMITER //
CREATE TRIGGER no_overselling
BEFORE INSERT ON orders
FOR EACH ROW
BEGIN
    IF NEW.number > (SELECT quantity FROM items WHERE name = NEW.item_name) THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Not enough stock';
    END IF;
END //
DELIMITER ;
