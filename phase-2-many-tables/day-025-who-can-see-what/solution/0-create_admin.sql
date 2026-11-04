-- Create the user rw_admin (any host, password rw_admin_dev) if it doesn't exist, with every privilege on every database.
CREATE USER IF NOT EXISTS 'rw_admin'@'%' IDENTIFIED BY 'rw_admin_dev';
GRANT ALL PRIVILEGES ON *.* TO 'rw_admin'@'%';
