-- For each table in this database: table_name, table_rows (InnoDB's estimate), data_pages (the clustered
-- index: data_length divided by the page size) and index_pages (the secondary indexes: index_length divided by
-- the page size). Alphabetical.
-- Write your statement below this line.
SELECT table_name AS table_name, table_rows AS table_rows,
       data_length DIV @@innodb_page_size AS data_pages,
       index_length DIV @@innodb_page_size AS index_pages
FROM information_schema.tables
WHERE table_schema = DATABASE()
ORDER BY table_name;
