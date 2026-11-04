-- Create the user rw_app (any host, password rw_app_dev) if missing. In riverwood_ops it may read, add and change rows, but never delete them.
CREATE USER IF NOT EXISTS 'rw_app'@'%' IDENTIFIED BY 'rw_app_dev';
GRANT SELECT, INSERT, UPDATE ON riverwood_ops.* TO 'rw_app'@'%';
