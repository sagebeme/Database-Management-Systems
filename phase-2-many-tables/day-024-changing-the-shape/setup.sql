-- Riverwood Plus subscribers, as the first version of the app left them (made-up people).
--   tools/mysql.sh riverwood < phase-2-many-tables/day-024-changing-the-shape/setup.sql
DROP TABLE IF EXISTS session_log, old_promo_codes, subscribers;

CREATE TABLE subscribers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(20) NOT NULL,
    phone VARCHAR(12),
    plan VARCHAR(10)
);
INSERT INTO subscribers (name, phone, plan) VALUES
    ('Akinyi Odhiambo', '254711000101', 'premium'),
    ('Baraka Mwangi', '254722000202', 'basic'),
    ('Chebet Kiprono', '254733000303', NULL),
    ('Dennis Otieno', '254744000404', 'family'),
    ('Esther Wanjiru', '254755000505', NULL),
    ('Faith Muthoni', NULL, 'basic');

CREATE TABLE old_promo_codes (
    code VARCHAR(12) PRIMARY KEY,
    percent_off TINYINT NOT NULL
);
INSERT INTO old_promo_codes VALUES ('MADARAKA20', 20), ('JAMHURI15', 15), ('NEWYEAR10', 10);

CREATE TABLE session_log (
    id INT AUTO_INCREMENT PRIMARY KEY,
    subscriber_id INT NOT NULL,
    started_at DATETIME NOT NULL
);
INSERT INTO session_log (subscriber_id, started_at) VALUES
    (1, '2026-10-01 20:15:00'), (2, '2026-10-01 21:02:00'), (1, '2026-10-02 19:40:00'),
    (4, '2026-10-02 22:10:00'), (3, '2026-10-03 18:05:00'), (1, '2026-10-03 20:30:00');
