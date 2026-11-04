-- A unique index, uq_result, so a student has at most one result per subject per exam, and an index,
-- idx_results_exam, for looking up an exam's results by exam and then student.
-- Write your statement below this line.
CREATE UNIQUE INDEX uq_result ON results (student_id, subject_id, exam_id);
CREATE INDEX idx_results_exam ON results (exam_id, student_id);
