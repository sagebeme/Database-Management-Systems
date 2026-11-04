-- A procedure, CountCorrections(user_id, OUT how_many): put the number of corrections that user has into
-- how_many. Safe to run twice.
-- Write your statement below this line.
DROP PROCEDURE IF EXISTS CountCorrections;
DELIMITER //
CREATE PROCEDURE CountCorrections(IN p_user_id INT, OUT how_many INT)
BEGIN
    SELECT COUNT(*) INTO how_many FROM corrections WHERE user_id = p_user_id;
END //
DELIMITER ;
