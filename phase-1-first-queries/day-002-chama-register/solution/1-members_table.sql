-- Create the members table (see the README for its columns), without an error if it exists.
CREATE TABLE IF NOT EXISTS members (
    id INT,
    full_name VARCHAR(100),
    phone VARCHAR(12),
    joined_on DATE,
    monthly_contribution DECIMAL(8, 2),
    is_official BOOLEAN
);
