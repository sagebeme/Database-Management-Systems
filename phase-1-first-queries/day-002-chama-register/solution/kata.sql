-- Kata: Table Count. Print how many tables the current database has, in a column called tables.
SELECT COUNT(*) AS tables
FROM information_schema.tables
WHERE table_schema = DATABASE();
