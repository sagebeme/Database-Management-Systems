-- A trigger, reset_valid_email: when a user's email changes, set valid_email back to 0 (they must confirm the
-- new address). Any other change leaves valid_email alone. Safe to run twice.
-- Write your statement below this line.
DROP TRIGGER IF EXISTS reset_valid_email;
DELIMITER //
CREATE TRIGGER reset_valid_email
BEFORE UPDATE ON users
FOR EACH ROW
BEGIN
    IF NEW.email <> OLD.email THEN
        SET NEW.valid_email = 0;
    END IF;
END //
DELIMITER ;
