-- A procedure, ComputeAverageWeightedScoreForUsers(): loop over every user with a CURSOR and call
-- ComputeAverageWeightedScoreForUser for each (that procedure is already installed). Safe to run twice.
-- Write your statement below this line.
DROP PROCEDURE IF EXISTS ComputeAverageWeightedScoreForUsers;
DELIMITER //
CREATE PROCEDURE ComputeAverageWeightedScoreForUsers()
BEGIN
    DECLARE done BOOLEAN DEFAULT FALSE;
    DECLARE next_id INT;
    DECLARE everyone CURSOR FOR SELECT id FROM users;
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = TRUE;

    OPEN everyone;
    read_loop: LOOP
        FETCH everyone INTO next_id;
        IF done THEN
            LEAVE read_loop;
        END IF;
        CALL ComputeAverageWeightedScoreForUser(next_id);
    END LOOP;
    CLOSE everyone;
END //
DELIMITER ;
