-- Pamoja, a chama app (invented), and its first sign-ups, collected on a web form with no rules at all.
--   tools/mysql.sh pamoja < phase-5-advanced-mysql/day-053-unique-users/setup.sql
DROP TABLE IF EXISTS signups;
CREATE TABLE signups (
    id INT PRIMARY KEY,
    email VARCHAR(255) NOT NULL,
    name VARCHAR(60) NOT NULL
);
INSERT INTO signups VALUES
    (1, 'wanjiku@pamoja.test', 'Wanjiku'),
    (2, 'otieno@pamoja.test', 'Otieno'),
    (3, 'Wanjiku@Pamoja.test', 'Wanjiku K'),
    (4, 'chebet@pamoja.test', 'Chebet'),
    (5, ' otieno@pamoja.test', 'Otieno O'),
    (6, 'mutua@pamoja.test', 'Mutua'),
    (7, 'WANJIKU@PAMOJA.TEST ', 'Wanjiku Kamau'),
    (8, 'akinyi@pamoja.test', 'Akinyi');
