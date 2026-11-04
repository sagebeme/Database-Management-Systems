-- A table stages: id, an INT the database numbers itself and that nobody can set by hand (an identity column,
-- GENERATED ALWAYS), and the primary key; name, TEXT, required and unique; county, TEXT, required, 'Nairobi'
-- unless you say otherwise.
-- Write your statement below this line.
CREATE TABLE stages (
    id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name TEXT NOT NULL UNIQUE,
    county TEXT NOT NULL DEFAULT 'Nairobi'
);
