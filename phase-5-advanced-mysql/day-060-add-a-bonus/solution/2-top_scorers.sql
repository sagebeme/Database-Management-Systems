-- A procedure, TopScorers(how_many): return the best how_many single scores: name, project, score.
-- Highest first, ties by name, then project. Safe to run twice.
-- Write your statement below this line.
DROP PROCEDURE IF EXISTS TopScorers;
DELIMITER //
CREATE PROCEDURE TopScorers(IN how_many INT)
BEGIN
    SELECT u.name, p.name AS project, c.score
    FROM corrections AS c
    JOIN users AS u ON u.id = c.user_id
    JOIN projects AS p ON p.id = c.project_id
    ORDER BY c.score DESC, u.name, p.name
    LIMIT how_many;
END //
DELIMITER ;
