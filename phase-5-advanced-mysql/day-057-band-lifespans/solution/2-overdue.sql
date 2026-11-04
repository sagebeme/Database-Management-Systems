-- Loans that came back late, or are still out and late on 2026-03-31: id, name (the member), days_late
-- (counted to the return day, or to 2026-03-31 if still out), fine (10 shillings a day, at most 500).
-- Most days late first, ties by id.
-- Write your statement below this line.
SELECT l.id, m.name, DATEDIFF(COALESCE(l.returned_on, '2026-03-31'), l.borrowed_on + INTERVAL 14 DAY) AS days_late,
       LEAST(10 * DATEDIFF(COALESCE(l.returned_on, '2026-03-31'), l.borrowed_on + INTERVAL 14 DAY), 500) AS fine
FROM loans AS l
JOIN members AS m ON m.id = l.member_id
WHERE DATEDIFF(COALESCE(l.returned_on, '2026-03-31'), l.borrowed_on + INTERVAL 14 DAY) > 0
ORDER BY days_late DESC, l.id;
