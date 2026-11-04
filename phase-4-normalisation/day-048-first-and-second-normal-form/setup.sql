-- A chama's member list as it came from a spreadsheet: several phones in one cell (invented people).
--   tools/mysql.sh chama < phase-4-normalisation/day-048-first-and-second-normal-form/setup.sql
DROP TABLE IF EXISTS member_phones, members_raw;
CREATE TABLE members_raw (
    id INT PRIMARY KEY,
    name VARCHAR(40) NOT NULL,
    phones VARCHAR(200) NULL
);
INSERT INTO members_raw VALUES
    (1, 'Wanjiku', '254711000001, 254722000001'),
    (2, 'Otieno', '254733000002'),
    (3, 'Chebet', '254711000003,254744000003 , 254755000003'),
    (4, 'Mutua', NULL),
    (5, 'Akinyi', '254766000005');
