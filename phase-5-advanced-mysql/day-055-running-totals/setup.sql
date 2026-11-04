-- Two kiosks' daily M-Pesa takings for two weeks of March 2026, in shillings (invented). Kawangware Fresh
-- closes on Sundays (8 and 15 March), so it has no row for those days.
--   tools/mysql.sh tills < phase-5-advanced-mysql/day-055-running-totals/setup.sql
DROP TABLE IF EXISTS takings;
CREATE TABLE takings (
    till VARCHAR(40) NOT NULL,
    day DATE NOT NULL,
    amount INT NOT NULL,
    PRIMARY KEY (till, day)
);
INSERT INTO takings VALUES
    ('Kawangware Fresh', '2026-03-02', 4000),
    ('Kawangware Fresh', '2026-03-03', 4700),
    ('Kawangware Fresh', '2026-03-04', 4400),
    ('Kawangware Fresh', '2026-03-05', 8200),
    ('Kawangware Fresh', '2026-03-06', 5400),
    ('Kawangware Fresh', '2026-03-07', 8800),
    ('Kawangware Fresh', '2026-03-09', 4000),
    ('Kawangware Fresh', '2026-03-10', 8200),
    ('Kawangware Fresh', '2026-03-11', 4600),
    ('Kawangware Fresh', '2026-03-12', 5400),
    ('Kawangware Fresh', '2026-03-13', 4000),
    ('Kawangware Fresh', '2026-03-14', 5700),
    ('Thika Road Duka', '2026-03-02', 5600),
    ('Thika Road Duka', '2026-03-03', 5200),
    ('Thika Road Duka', '2026-03-04', 4000),
    ('Thika Road Duka', '2026-03-05', 4400),
    ('Thika Road Duka', '2026-03-06', 3400),
    ('Thika Road Duka', '2026-03-07', 3400),
    ('Thika Road Duka', '2026-03-08', 4200),
    ('Thika Road Duka', '2026-03-09', 3500),
    ('Thika Road Duka', '2026-03-10', 3000),
    ('Thika Road Duka', '2026-03-11', 5600),
    ('Thika Road Duka', '2026-03-12', 3700),
    ('Thika Road Duka', '2026-03-13', 4400),
    ('Thika Road Duka', '2026-03-14', 5900),
    ('Thika Road Duka', '2026-03-15', 5000);
