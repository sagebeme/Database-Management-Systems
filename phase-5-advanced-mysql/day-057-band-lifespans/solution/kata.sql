-- Each member's next birthday on or after 2026-03-31 (today counts), and how many days away it is:
-- name, next_birthday, days_to_go. Soonest first, ties by name.
-- Write your statement below this line.
SELECT name, next_birthday, DATEDIFF(next_birthday, '2026-03-31') AS days_to_go
FROM (
    SELECT name,
           CASE
               WHEN born_on + INTERVAL TIMESTAMPDIFF(YEAR, born_on, '2026-03-31') YEAR >= '2026-03-31'
                   THEN born_on + INTERVAL TIMESTAMPDIFF(YEAR, born_on, '2026-03-31') YEAR
               ELSE born_on + INTERVAL TIMESTAMPDIFF(YEAR, born_on, '2026-03-31') + 1 YEAR
           END AS next_birthday
    FROM members
) AS b
ORDER BY days_to_go, name;
