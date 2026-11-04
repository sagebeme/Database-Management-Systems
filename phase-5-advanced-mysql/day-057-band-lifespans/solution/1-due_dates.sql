-- Every loan's due date (14 days after it was borrowed) and the weekday it falls on:
-- id, borrowed_on, due_on, due_day (Monday, Tuesday, ...). By id.
-- Write your statement below this line.
SELECT id, borrowed_on, borrowed_on + INTERVAL 14 DAY AS due_on, DAYNAME(borrowed_on + INTERVAL 14 DAY) AS due_day
FROM loans
ORDER BY id;
