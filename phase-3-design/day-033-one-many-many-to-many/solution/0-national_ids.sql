-- Create national_ids: id_no (CHAR(8), primary key) and person_id (a real person).
-- A person holds at most one ID, and every ID belongs to exactly one person.
CREATE TABLE IF NOT EXISTS national_ids (
    id_no CHAR(8) PRIMARY KEY,
    person_id INT NOT NULL UNIQUE,
    FOREIGN KEY (person_id) REFERENCES persons (id)
);
