-- paid_on and total (the sum of amount) for each day of March 2026, by date: written so Postgres reads only the
-- March partition.
SELECT paid_on, sum(amount) AS total
FROM payments
WHERE paid_on >= '2026-03-01' AND paid_on < '2026-04-01'
GROUP BY paid_on
ORDER BY paid_on;
