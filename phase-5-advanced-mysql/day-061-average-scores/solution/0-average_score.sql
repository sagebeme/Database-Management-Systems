-- A procedure, ComputeAverageScoreForUser(user_id): store that user's average score in users.average_score
-- (0 if they have no corrections). Safe to run twice.
-- Write your statement below this line.
DROP PROCEDURE IF EXISTS ComputeAverageScoreForUser;
DELIMITER //
CREATE PROCEDURE ComputeAverageScoreForUser(IN p_user_id INT)
BEGIN
    UPDATE users
    SET average_score = COALESCE((SELECT AVG(score) FROM corrections WHERE user_id = p_user_id), 0)
    WHERE id = p_user_id;
END //
DELIMITER ;
