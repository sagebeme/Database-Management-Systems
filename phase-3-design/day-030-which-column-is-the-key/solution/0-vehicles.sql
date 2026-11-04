-- Create vehicles: reg_no (CHAR(8), the primary key), chassis_no (CHAR(17), required, unique: the alternate key),
-- sacco_id (required, a real sacco) and seats (TINYINT, required).
CREATE TABLE IF NOT EXISTS vehicles (
    reg_no CHAR(8) PRIMARY KEY,
    chassis_no CHAR(17) NOT NULL UNIQUE,
    sacco_id INT NOT NULL,
    seats TINYINT NOT NULL,
    FOREIGN KEY (sacco_id) REFERENCES saccos (id)
);
