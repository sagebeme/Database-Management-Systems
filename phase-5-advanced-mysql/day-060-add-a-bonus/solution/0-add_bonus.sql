-- A procedure, AddBonus(user_id, project_name, score): add a correction for that user and project, creating
-- the project first if there's no project with that name. Safe to run twice.
-- Write your statement below this line.
DROP PROCEDURE IF EXISTS AddBonus;
DELIMITER //
CREATE PROCEDURE AddBonus(IN p_user_id INT, IN p_project_name VARCHAR(60), IN p_score INT)
BEGIN
    INSERT INTO projects (name)
    SELECT p_project_name FROM DUAL
    WHERE NOT EXISTS (SELECT 1 FROM projects WHERE name = p_project_name);

    INSERT INTO corrections (user_id, project_id, score)
    SELECT p_user_id, id, p_score FROM projects WHERE name = p_project_name;
END //
DELIMITER ;
