-- A procedure, ComputeAllInOneGo(): the same result as ComputeAverageWeightedScoreForUsers, for every user,
-- in one UPDATE statement: no cursor, no loop. Safe to run twice.
-- Write your statement below this line.
DROP PROCEDURE IF EXISTS ComputeAllInOneGo;
DELIMITER //
CREATE PROCEDURE ComputeAllInOneGo()
BEGIN
    UPDATE users AS u
    LEFT JOIN (
        SELECT c.user_id, SUM(c.score * p.weight) / SUM(p.weight) AS weighted
        FROM corrections AS c
        JOIN projects AS p ON p.id = c.project_id
        GROUP BY c.user_id
    ) AS w ON w.user_id = u.id
    SET u.average_score = COALESCE(w.weighted, 0);
END //
DELIMITER ;
