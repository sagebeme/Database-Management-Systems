-- A function Grade(score) (A from 80, B from 65, C from 50, D from 40, else E), two triggers,
-- grade_on_insert and grade_on_update, that keep results.grade equal to Grade(score), and fill in the grades of
-- the results already there. Safe to run twice.
-- Write your statement below this line.
DROP FUNCTION IF EXISTS Grade;
DROP TRIGGER IF EXISTS grade_on_insert;
DROP TRIGGER IF EXISTS grade_on_update;
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
CREATE TRIGGER grade_on_insert BEFORE INSERT ON results FOR EACH ROW SET NEW.grade = Grade(NEW.score);
CREATE TRIGGER grade_on_update BEFORE UPDATE ON results FOR EACH ROW SET NEW.grade = Grade(NEW.score);
UPDATE results SET grade = Grade(score);
