-- A trigger, record_email_change: after an update that changes a user's email, add a row to email_history
-- (user_id, old_email, new_email). Safe to run twice.
-- Write your statement below this line.
DROP TRIGGER IF EXISTS record_email_change;
DELIMITER //
CREATE TRIGGER record_email_change
AFTER UPDATE ON users
FOR EACH ROW
BEGIN
    IF NEW.email <> OLD.email THEN
        INSERT INTO email_history (user_id, old_email, new_email) VALUES (OLD.id, OLD.email, NEW.email);
    END IF;
END //
DELIMITER ;
