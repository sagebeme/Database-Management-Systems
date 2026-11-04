WITH RECURSIVE chain AS (
    SELECT id AS rider_id, id AS root_id, 0 AS depth FROM riders WHERE referred_by IS NULL
    UNION ALL
    SELECT r.id, c.root_id, c.depth + 1
    FROM riders r JOIN chain c ON r.referred_by = c.rider_id
)
SELECT rider_id, root_id, depth FROM chain ORDER BY rider_id;
