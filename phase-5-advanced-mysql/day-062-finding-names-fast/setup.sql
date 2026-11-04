-- 50,000 names with scores, and 50,000 orders, made up by a recursive CTE (Day 56) so the file stays small.
-- The same rows every time: nothing here is random.
--   tools/mysql.sh fast < phase-5-advanced-mysql/day-062-finding-names-fast/setup.sql
DROP TABLE IF EXISTS names, orders;
CREATE TABLE names (
    name VARCHAR(255),
    score INT
);
CREATE TABLE orders (
    id INT PRIMARY KEY,
    customer_id INT NOT NULL,
    placed_on DATE NOT NULL,
    total INT NOT NULL
);
SET SESSION cte_max_recursion_depth = 50000;
INSERT INTO names (name, score)
WITH RECURSIVE n AS (SELECT 1 AS i UNION ALL SELECT i + 1 FROM n WHERE i < 50000)
SELECT CONCAT(ELT(1 + (i * 7) % 20, 'Wanjiku', 'Otieno', 'Chebet', 'Mutua', 'Akinyi', 'Kamau', 'Njeri', 'Kiprop',
                  'Achieng', 'Mwangi', 'Wairimu', 'Omondi', 'Jepkosgei', 'Mumbua', 'Barasa', 'Nyambura', 'Kibet',
                  'Atieno', 'Zawadi', 'Halima'),
              ' ', i),
       (i * 37) % 101
FROM n;
INSERT INTO orders (id, customer_id, placed_on, total)
WITH RECURSIVE n AS (SELECT 1 AS i UNION ALL SELECT i + 1 FROM n WHERE i < 50000)
SELECT i, 1 + (i * 7919) % 5000, '2023-01-01' + INTERVAL (i * 13) % 1186 DAY, 100 + (i * 31) % 9900
FROM n;
ANALYZE TABLE names, orders;
