-- A procedure, ReportCard(student_name, exam_name): that student's results in that exam: subject, score,
-- grade, in subject name order. Safe to run twice.
-- Write your statement below this line.
DROP PROCEDURE IF EXISTS ReportCard;
DELIMITER //
CREATE PROCEDURE ReportCard(IN p_student VARCHAR(60), IN p_exam VARCHAR(30))
BEGIN
    SELECT sub.name AS subject, r.score, r.grade
    FROM results AS r
    JOIN students AS s ON s.id = r.student_id
    JOIN exams AS e ON e.id = r.exam_id
    JOIN subjects AS sub ON sub.id = r.subject_id
    WHERE s.name = p_student AND e.name = p_exam
    ORDER BY sub.name;
END //
DELIMITER ;
