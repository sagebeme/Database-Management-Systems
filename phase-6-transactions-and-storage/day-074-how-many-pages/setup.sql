-- 20,000 SACCO members, made up by a recursive CTE so the file stays small. The same rows every time.
--   tools/mysql.sh pages < phase-6-transactions-and-storage/day-074-how-many-pages/setup.sql
DROP TABLE IF EXISTS members, loans;
CREATE TABLE members (
    id INT PRIMARY KEY,
    phone CHAR(12) NOT NULL,
    name VARCHAR(40) NOT NULL,
    joined DATE NOT NULL,
    savings INT NOT NULL,
    INDEX idx_phone (phone)
);
CREATE TABLE loans (
    id INT PRIMARY KEY,
    member_id INT NOT NULL,
    amount INT NOT NULL,
    notes VARCHAR(500) NOT NULL
);
SET SESSION cte_max_recursion_depth = 20000;
INSERT INTO members (id, phone, name, joined, savings)
WITH RECURSIVE n AS (SELECT 1 AS i UNION ALL SELECT i + 1 FROM n WHERE i < 20000)
SELECT i, CONCAT('2547', LPAD((i * 7919) % 100000000, 8, '0')),
       CONCAT(ELT(1 + (i * 7) % 10, 'Wanjiku', 'Otieno', 'Chebet', 'Mutua', 'Akinyi', 'Kamau', 'Njeri', 'Kiprop',
                  'Achieng', 'Mwangi'), ' ', i),
       '2015-01-01' + INTERVAL (i * 13) % 4000 DAY, (i * 37) % 250000
FROM n;
INSERT INTO loans (id, member_id, amount, notes)
WITH RECURSIVE n AS (SELECT 1 AS i UNION ALL SELECT i + 1 FROM n WHERE i < 5000)
SELECT i, 1 + (i * 31) % 20000, 1000 * (1 + i % 200), REPEAT('Guarantors signed. ', 20)
FROM n;
ANALYZE TABLE members, loans;
