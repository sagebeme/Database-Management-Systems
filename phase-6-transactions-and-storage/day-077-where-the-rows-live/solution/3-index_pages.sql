-- For each index on members: index_name and pages (its size in pages, from mysql.innodb_index_stats, where
-- stat_name is 'size'). Alphabetical by index name. Run ANALYZE TABLE first if the numbers look stale.
-- Write your statement below this line.
SELECT index_name, stat_value AS pages
FROM mysql.innodb_index_stats
WHERE database_name = DATABASE() AND table_name = 'members' AND stat_name = 'size'
ORDER BY index_name;
