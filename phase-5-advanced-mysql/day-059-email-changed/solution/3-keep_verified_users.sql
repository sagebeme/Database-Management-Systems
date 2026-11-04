-- A trigger, keep_verified_users: refuse to delete a user whose email is confirmed, with SQLSTATE '45000' and
-- the message 'Verified users cannot be deleted'. Unconfirmed users can be deleted. Safe to run twice.
-- Write your statement below this line.
DROP TRIGGER IF EXISTS keep_verified_users;
DELIMITER //
CREATE TRIGGER keep_verified_users
BEFORE DELETE ON users
FOR EACH ROW
BEGIN
    IF OLD.valid_email THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Verified users cannot be deleted';
    END IF;
END //
DELIMITER ;
