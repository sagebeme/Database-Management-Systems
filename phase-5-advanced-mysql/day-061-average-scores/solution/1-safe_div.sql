-- A function, SafeDiv(a, b): a divided by b, or 0 when b is 0. Safe to run twice.
-- Write your statement below this line.
DROP FUNCTION IF EXISTS SafeDiv;
DELIMITER //
CREATE FUNCTION SafeDiv(a INT, b INT)
RETURNS FLOAT
DETERMINISTIC
BEGIN
    IF b = 0 THEN
        RETURN 0;
    END IF;
    RETURN a / b;
END //
DELIMITER ;
