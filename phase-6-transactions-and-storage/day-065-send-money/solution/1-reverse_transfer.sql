-- A procedure, ReverseTransfer(transfer_id), in one transaction: send the money back and mark the transfer
-- reversed. Refuse with SQLSTATE '45000', changing nothing: 'No such transfer', 'Already reversed', or
-- 'Insufficient funds' (the receiver has spent it). Safe to run twice.
-- Write your statement below this line.
DROP PROCEDURE IF EXISTS ReverseTransfer;
DELIMITER //
CREATE PROCEDURE ReverseTransfer(IN p_id INT)
BEGIN
    DECLARE v_from CHAR(12);
    DECLARE v_to CHAR(12);
    DECLARE v_amount INT;
    DECLARE v_reversed BOOLEAN;
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
        RESIGNAL;
    END;

    START TRANSACTION;
    SELECT from_phone, to_phone, amount, reversed INTO v_from, v_to, v_amount, v_reversed
    FROM transfers WHERE id = p_id FOR UPDATE;
    IF v_from IS NULL THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'No such transfer';
    END IF;
    IF v_reversed THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Already reversed';
    END IF;
    UPDATE accounts SET balance = balance - v_amount WHERE phone = v_to AND balance >= v_amount;
    IF ROW_COUNT() = 0 THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Insufficient funds';
    END IF;
    UPDATE accounts SET balance = balance + v_amount WHERE phone = v_from;
    UPDATE transfers SET reversed = 1 WHERE id = p_id;
    COMMIT;
END //
DELIMITER ;
