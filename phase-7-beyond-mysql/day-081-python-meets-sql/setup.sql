-- A SACCO's members and the transfers between them. Made-up people.
--   tools/psql.sh sacco -f phase-7-beyond-mysql/day-081-python-meets-sql/setup.sql
DROP TABLE IF EXISTS transfers, members;
CREATE TABLE members (
    id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name TEXT NOT NULL,
    phone TEXT NOT NULL UNIQUE,
    county TEXT NOT NULL,
    savings INT NOT NULL DEFAULT 0 CHECK (savings >= 0)
);
CREATE TABLE transfers (
    id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    from_id INT NOT NULL REFERENCES members (id),
    to_id INT NOT NULL REFERENCES members (id),
    amount INT NOT NULL CHECK (amount > 0),
    at TIMESTAMPTZ NOT NULL DEFAULT now()
);
INSERT INTO members (name, phone, county, savings) VALUES
    ('Wanjiku Kamau', '254711000001', 'Kiambu', 42000),
    ('Otieno Ochieng', '254722000002', 'Kisumu', 15500),
    ('Ng''ang''a Mwangi', '254733000003', 'Nyeri', 8000),
    ('Chebet Kiprop', '254744000004', 'Uasin Gishu', 61000),
    ('Akinyi Atieno', '254755000005', 'Kisumu', 3000),
    ('Mutua Musyoka', '254766000006', 'Machakos', 27500),
    ('Wanjiku Njeri', '254777000007', 'Nairobi', 12000);
