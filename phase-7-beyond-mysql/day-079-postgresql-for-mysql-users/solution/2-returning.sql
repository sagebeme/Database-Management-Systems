-- Add the sacco 'Mji Movers' and print its new id and name, in the same statement.
-- Write your statement below this line.
INSERT INTO saccos (name) VALUES ('Mji Movers') RETURNING id, name;
