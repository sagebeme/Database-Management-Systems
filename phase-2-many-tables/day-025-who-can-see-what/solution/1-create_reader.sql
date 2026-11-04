-- Create the database riverwood_ops and the user rw_reader (any host, password rw_reader_dev), both only if missing. rw_reader may only read riverwood_ops.
CREATE DATABASE IF NOT EXISTS riverwood_ops;
CREATE USER IF NOT EXISTS 'rw_reader'@'%' IDENTIFIED BY 'rw_reader_dev';
GRANT SELECT ON riverwood_ops.* TO 'rw_reader'@'%';
