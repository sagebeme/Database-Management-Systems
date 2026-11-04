-- Code and time of every transaction in March 2025.
SELECT code, happened_at FROM transactions
WHERE happened_at >= '2025-03-01' AND happened_at < '2025-04-01';
