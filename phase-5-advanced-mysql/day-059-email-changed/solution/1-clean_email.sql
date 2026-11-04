-- Two triggers that store every email trimmed and in lower case: clean_email_insert (on insert) and
-- clean_email_update (on update). The update one must run before reset_valid_email, so ' wanjiku@pamoja.test'
-- doesn't count as a new address. Safe to run twice.
-- Write your statement below this line.
DROP TRIGGER IF EXISTS clean_email_insert;
DROP TRIGGER IF EXISTS clean_email_update;
CREATE TRIGGER clean_email_insert
BEFORE INSERT ON users
FOR EACH ROW
SET NEW.email = LOWER(TRIM(NEW.email));
CREATE TRIGGER clean_email_update
BEFORE UPDATE ON users
FOR EACH ROW PRECEDES reset_valid_email
SET NEW.email = LOWER(TRIM(NEW.email));
