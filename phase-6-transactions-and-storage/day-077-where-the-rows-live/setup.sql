-- 20,000 SACCO members in ten counties, made up by a recursive CTE. The same rows every time.
-- Every phone is 2547 and 8 digits worked out from the id: member 1 is 254700007919.
--   tools/mysql.sh clustered < phase-6-transactions-and-storage/day-077-where-the-rows-live/setup.sql
DROP TABLE IF EXISTS members;
CREATE TABLE members (
    id INT PRIMARY KEY,
    phone CHAR(12) NOT NULL,
    name VARCHAR(40) NOT NULL,
    county VARCHAR(20) NOT NULL,
    savings INT NOT NULL
);
SET SESSION cte_max_recursion_depth = 20000;
INSERT INTO members (id, phone, name, county, savings)
WITH RECURSIVE n AS (SELECT 1 AS i UNION ALL SELECT i + 1 FROM n WHERE i < 20000)
SELECT i, CONCAT('2547', LPAD((i * 7919) % 100000000, 8, '0')),
       CONCAT(ELT(1 + (i * 7) % 10, 'Wanjiku', 'Otieno', 'Chebet', 'Mutua', 'Akinyi', 'Kamau', 'Njeri', 'Kiprop',
                  'Achieng', 'Mwangi'), ' ', i),
       ELT(1 + (i * 3) % 10, 'Nairobi', 'Mombasa', 'Kisumu', 'Nakuru', 'Eldoret', 'Kiambu', 'Machakos', 'Nyeri',
           'Kakamega', 'Kisii'),
       (i * 37) % 250000
FROM n;
ANALYZE TABLE members;
