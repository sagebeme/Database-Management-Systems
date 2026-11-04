SELECT id + 1 AS gap_start, next_id - 1 AS gap_end
FROM (SELECT id, lead(id) OVER (ORDER BY id) AS next_id FROM trips) t
WHERE next_id > id + 1
UNION ALL
SELECT 1, min(id) - 1 FROM trips HAVING min(id) > 1
ORDER BY gap_start;
