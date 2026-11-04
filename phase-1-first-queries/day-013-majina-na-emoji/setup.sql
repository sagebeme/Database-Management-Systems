-- The guest list for a wedding in Nyeri, in a table made years ago with the old latin1
-- character set. latin1 can hold é, but not emoji or most of the world's alphabets.
-- Names are made up.
--   tools/mysql.sh harusi < phase-1-first-queries/day-013-majina-na-emoji/setup.sql
DROP TABLE IF EXISTS guests;
CREATE TABLE guests (
    id INT,
    name VARCHAR(60),
    side VARCHAR(10)
) CHARACTER SET latin1 COLLATE latin1_swedish_ci;
INSERT INTO guests (id, name, side) VALUES
    (1, 'Amina Hassan', 'bride'),
    (2, 'AMINA KARIUKI', 'groom'),
    (3, 'Renée Achieng', 'bride'),
    (4, 'Renee Otieno', 'groom'),
    (5, 'José Mwangi', 'groom'),
    (6, 'Wairimu Ndung''u', 'bride');
