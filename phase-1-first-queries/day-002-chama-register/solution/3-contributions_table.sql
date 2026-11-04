-- Create the contributions table (see the README), without an error if it exists.
CREATE TABLE IF NOT EXISTS contributions (
    member_id INT,
    amount DECIMAL(10, 2),
    paid_at DATETIME,
    mpesa_code CHAR(10)
);
