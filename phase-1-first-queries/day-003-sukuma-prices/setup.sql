-- Mama Wanjiru's price list. Load it with:
--   tools/mysql.sh mama_mboga < phase-1-first-queries/day-003-sukuma-prices/setup.sql
DROP TABLE IF EXISTS produce;
CREATE TABLE produce (
    id INT,
    name VARCHAR(50),
    unit VARCHAR(10),
    price_kes DECIMAL(7, 2)
);
INSERT INTO produce (id, name, unit, price_kes) VALUES
    (1, 'Tomatoes', 'kg', 120.00),
    (2, 'Onions', 'kg', 90.00),
    (3, 'Managu', 'bunch', 30.00),
    (4, 'Avocado', 'piece', 15.00);
