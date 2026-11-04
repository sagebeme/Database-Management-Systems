-- A procedure, RenameProject(old_name, new_name). Refuse (SQLSTATE '45000') with the message
-- 'No such project' if old_name doesn't exist, or 'Name already taken' if another project has new_name.
-- Safe to run twice.
-- Write your statement below this line.
DROP PROCEDURE IF EXISTS RenameProject;
DELIMITER //
CREATE PROCEDURE RenameProject(IN old_name VARCHAR(60), IN new_name VARCHAR(60))
BEGIN
    DECLARE project INT DEFAULT NULL;
    SELECT id INTO project FROM projects WHERE name = old_name;
    IF project IS NULL THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'No such project';
    END IF;
    IF EXISTS (SELECT 1 FROM projects WHERE name = new_name AND id <> project) THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Name already taken';
    END IF;
    UPDATE projects SET name = new_name WHERE id = project;
END //
DELIMITER ;
