-- For every column of guests: column_name, character_set_name and collation_name, in column order (text columns have a character set, others show NULL).
SELECT column_name, character_set_name, collation_name
FROM information_schema.columns
WHERE table_schema = DATABASE() AND table_name = 'guests'
ORDER BY ordinal_position;
