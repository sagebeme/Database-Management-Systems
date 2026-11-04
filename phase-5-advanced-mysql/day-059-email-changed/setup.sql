-- Pamoja's users (invented). valid_email is 1 once someone has clicked the link in the welcome email.
--   tools/mysql.sh pamoja < phase-5-advanced-mysql/day-059-email-changed/setup.sql
DROP TABLE IF EXISTS email_history, users;
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE,
    name VARCHAR(60),
    valid_email BOOLEAN NOT NULL DEFAULT 0
);
CREATE TABLE email_history (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    old_email VARCHAR(255) NOT NULL,
    new_email VARCHAR(255) NOT NULL,
    changed_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);
INSERT INTO users (email, name, valid_email) VALUES
    ('wanjiku@pamoja.test', 'Wanjiku', 1), ('otieno@pamoja.test', 'Otieno', 0), ('chebet@pamoja.test', 'Chebet', 1),
    ('mutua@pamoja.test', 'Mutua', 0), ('akinyi@pamoja.test', 'Akinyi', 1);
