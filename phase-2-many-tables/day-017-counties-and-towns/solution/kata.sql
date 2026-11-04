-- Kata: Who Points Here? Every table and column in this database that has a foreign key to counties: table_name and column_name, alphabetical.
SELECT table_name AS table_name, column_name AS column_name
FROM information_schema.key_column_usage
WHERE table_schema = DATABASE() AND referenced_table_name = 'counties'
ORDER BY table_name, column_name;
