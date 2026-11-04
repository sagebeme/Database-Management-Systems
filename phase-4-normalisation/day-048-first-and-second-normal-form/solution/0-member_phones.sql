-- First normal form: create member_phones (member_id -> members_raw, phone CHAR(12), the pair as the key)
-- and fill it with one row per phone, trimmed.
CREATE TABLE member_phones (
    member_id INT NOT NULL,
    phone CHAR(12) NOT NULL,
    PRIMARY KEY (member_id, phone),
    FOREIGN KEY (member_id) REFERENCES members_raw (id)
);
INSERT INTO member_phones (member_id, phone)
SELECT m.id, TRIM(j.phone)
FROM members_raw AS m,
     JSON_TABLE(CONCAT('["', REPLACE(m.phones, ',', '","'), '"]'), '$[*]' COLUMNS (phone VARCHAR(20) PATH '$')) AS j;
