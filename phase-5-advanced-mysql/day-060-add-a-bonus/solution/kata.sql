-- A procedure, CurveProject(project_name, target): if the project's average score is below target, add the same
-- whole number of points to every score on it (the difference, rounded to the nearest point), never going over
-- 100. If the average is already at or above target, change nothing. Safe to run twice.
-- Write your statement below this line.
DROP PROCEDURE IF EXISTS CurveProject;
DELIMITER //
CREATE PROCEDURE CurveProject(IN project_name VARCHAR(60), IN target INT)
BEGIN
    DECLARE project INT;
    DECLARE current_avg DECIMAL(6, 2);
    SELECT id INTO project FROM projects WHERE name = project_name;
    SELECT AVG(score) INTO current_avg FROM corrections WHERE project_id = project;
    IF current_avg < target THEN
        UPDATE corrections
        SET score = LEAST(score + ROUND(target - current_avg), 100)
        WHERE project_id = project;
    END IF;
END //
DELIMITER ;
