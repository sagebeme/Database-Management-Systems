-- The Umoja Women's Group register, with some mistakes in it. Names and numbers are made up.
--   tools/mysql.sh chama < phase-1-first-queries/day-007-fixing-the-register/setup.sql
DROP TABLE IF EXISTS members;
CREATE TABLE members (
    id INT,
    full_name VARCHAR(100),
    phone VARCHAR(12),
    county VARCHAR(30),
    monthly_contribution DECIMAL(8, 2),
    arrears_kes DECIMAL(8, 2),
    status VARCHAR(10)
);
INSERT INTO members (id, full_name, phone, county, monthly_contribution, arrears_kes, status) VALUES
    (1, 'Atieno Ouma', '254712000101', 'Kakamega', 500.00, 0.00, 'active'),
    (2, 'Nafula Wekesa', '254712000102', 'Kakamega', 1000.00, 1500.00, 'active'),
    (3, 'Akinyi Odera', '254712000103', 'Vihiga', 500.00, 0.00, 'left'),
    (4, 'Makokha Juma', '25471200010', 'Kakamega', 500.00, 2000.00, 'active'),
    (5, 'Imali Shikuku', '254712000105', 'Vihiga', 750.00, 500.00, 'active'),
    (6, 'Auma Were', '254712000106', 'Busia', 500.00, 0.00, 'left'),
    (7, 'Khaemba Simiyu', '254712000107', 'Kakamega', 1000.00, 1200.00, 'active'),
    (8, 'Nekesa Barasa', '254712000108', 'Bungoma', 500.00, 0.00, 'active');
