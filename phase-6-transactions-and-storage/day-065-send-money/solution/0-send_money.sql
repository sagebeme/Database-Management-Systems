-- A procedure, SendMoney(from_phone, to_phone, amount), all in one transaction: take the amount from the
-- sender, give it to the receiver, and record it in transfers. Refuse with SQLSTATE '45000' and one of these
-- messages, changing nothing: 'Amount must be positive', 'No such account' (either phone), 'Insufficient funds'.
-- If anything fails part-way, nothing it did may be kept. Safe to run twice.
-- Write your statement below this line.
DROP PROCEDURE IF EXISTS SendMoney;
DELIMITER //
CREATE PROCEDURE SendMoney(IN p_from CHAR(12), IN p_to CHAR(12), IN p_amount INT)
BEGIN
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
        RESIGNAL;
    END;

    START TRANSACTION;
    IF p_amount <= 0 THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Amount must be positive';
    END IF;
    IF (SELECT COUNT(*) FROM accounts WHERE phone IN (p_from, p_to)) < 2 THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'No such account';
    END IF;
    UPDATE accounts SET balance = balance - p_amount WHERE phone = p_from AND balance >= p_amount;
    IF ROW_COUNT() = 0 THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Insufficient funds';
    END IF;
    UPDATE accounts SET balance = balance + p_amount WHERE phone = p_to;
    INSERT INTO transfers (from_phone, to_phone, amount) VALUES (p_from, p_to, p_amount);
    COMMIT;
END //
DELIMITER ;
