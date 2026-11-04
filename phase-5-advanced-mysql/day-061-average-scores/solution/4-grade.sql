-- A function, Grade(score): 'A' for 80 and up, 'B' for 65 and up, 'C' for 50 and up, 'D' for 40 and up,
-- otherwise 'E'. Safe to run twice.
-- Write your statement below this line.
DROP FUNCTION IF EXISTS Grade;
DELIMITER //
CREATE FUNCTION Grade(score DECIMAL(5, 2))
RETURNS CHAR(1)
DETERMINISTIC
BEGIN
    RETURN CASE
        WHEN score >= 80 THEN 'A'
        WHEN score >= 65 THEN 'B'
        WHEN score >= 50 THEN 'C'
        WHEN score >= 40 THEN 'D'
        ELSE 'E'
    END;
END //
DELIMITER ;
