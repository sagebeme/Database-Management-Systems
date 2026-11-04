-- A procedure, ComputeAverageWeightedScoreForUser(user_id): store that user's weighted average in
-- users.average_score: each score times its project's weight, added up, divided by the weights added up
-- (0 if they have no corrections). Safe to run twice.
-- Write your statement below this line.
DROP PROCEDURE IF EXISTS ComputeAverageWeightedScoreForUser;
DELIMITER //
CREATE PROCEDURE ComputeAverageWeightedScoreForUser(IN p_user_id INT)
BEGIN
    UPDATE users
    SET average_score = COALESCE((
        SELECT SUM(c.score * p.weight) / SUM(p.weight)
        FROM corrections AS c
        JOIN projects AS p ON p.id = c.project_id
        WHERE c.user_id = p_user_id
    ), 0)
    WHERE id = p_user_id;
END //
DELIMITER ;
