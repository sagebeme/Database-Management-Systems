-- Taarab acts ranked by how long they lasted, or have lasted so far (to 2026 if they haven't split):
-- name, lifespan (whole years). Longest first, ties by name.
-- Write your statement below this line.
SELECT name, COALESCE(split, 2026) - formed AS lifespan
FROM artists
WHERE genre = 'Taarab'
ORDER BY lifespan DESC, name;
