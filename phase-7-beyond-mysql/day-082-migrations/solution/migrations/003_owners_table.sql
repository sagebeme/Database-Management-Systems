-- Move owners into their own table, keeping every vehicle's owner:
-- owners: id (identity, primary key), name (TEXT, required), phone (TEXT, required, unique), one row per phone,
-- numbered in phone order; vehicles.owner_id, required, referencing owners; and no vehicles.owner column.
CREATE TABLE owners (
    id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name TEXT NOT NULL,
    phone TEXT NOT NULL UNIQUE
);
INSERT INTO owners (name, phone)
SELECT DISTINCT split_part(owner, ' (', 1), rtrim(split_part(owner, ' (', 2), ')')
FROM vehicles
ORDER BY 2;
ALTER TABLE vehicles ADD COLUMN owner_id INT REFERENCES owners (id);
UPDATE vehicles AS v
SET owner_id = o.id
FROM owners AS o
WHERE o.phone = rtrim(split_part(v.owner, ' (', 2), ')');
ALTER TABLE vehicles ALTER COLUMN owner_id SET NOT NULL;
ALTER TABLE vehicles DROP COLUMN owner;
