-- vehicles: id (an identity column, the primary key), plate (TEXT, required, unique), owner (TEXT, required:
-- the owner's name and phone, like 'Wanjiku Kamau (254711000001)').
CREATE TABLE vehicles (
    id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    plate TEXT NOT NULL UNIQUE,
    owner TEXT NOT NULL
);
