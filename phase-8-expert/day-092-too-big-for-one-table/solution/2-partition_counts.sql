-- How many rows each partition holds: partition (its name, from tableoid) and payments, by partition name.
SELECT tableoid::regclass::text AS partition, count(*) AS payments FROM payments GROUP BY 1 ORDER BY 1;
