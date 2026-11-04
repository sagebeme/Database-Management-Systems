-- A trigger, limit_email_changes: refuse a user's fourth email change (three are allowed, counted in
-- email_history), with SQLSTATE '45000' and the message 'Too many email changes'. Other updates still work.
-- Safe to run twice.
-- Write your statement below this line.
DROP TRIGGER IF EXISTS limit_email_changes;
DELIMITER //
CREATE TRIGGER limit_email_changes
BEFORE UPDATE ON users
FOR EACH ROW
BEGIN
    IF NEW.email <> OLD.email
       AND (SELECT COUNT(*) FROM email_history WHERE user_id = OLD.id) >= 3 THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Too many email changes';
    END IF;
END //
DELIMITER ;
