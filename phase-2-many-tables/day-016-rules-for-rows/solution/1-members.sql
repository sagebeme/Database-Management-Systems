-- Create members (id INT, name VARCHAR(100), status VARCHAR(10)) where status is never empty and is active unless you say otherwise.
CREATE TABLE IF NOT EXISTS members (
    id INT,
    name VARCHAR(100),
    status VARCHAR(10) NOT NULL DEFAULT 'active'
);
