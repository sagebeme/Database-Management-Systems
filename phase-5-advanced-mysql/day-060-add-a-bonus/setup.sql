-- A coding school's marks (invented): users, projects, and each correction's score out of 100. Mutua has none yet.
--   tools/mysql.sh school < phase-5-advanced-mysql/day-060-add-a-bonus/setup.sql
DROP TABLE IF EXISTS corrections, projects, users;
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(60) NOT NULL,
    average_score DECIMAL(5, 2) NOT NULL DEFAULT 0
);
CREATE TABLE projects (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(60) NOT NULL UNIQUE,
    weight INT NOT NULL DEFAULT 1
);
CREATE TABLE corrections (
    user_id INT NOT NULL,
    project_id INT NOT NULL,
    score INT NOT NULL DEFAULT 0,
    FOREIGN KEY (user_id) REFERENCES users (id),
    FOREIGN KEY (project_id) REFERENCES projects (id)
);
INSERT INTO users (name) VALUES ('Wanjiku'), ('Otieno'), ('Chebet'), ('Mutua');
INSERT INTO projects (name, weight) VALUES ('SQL basics', 1), ('Joins', 2), ('Normalisation', 3);
INSERT INTO corrections (user_id, project_id, score) VALUES
    (1, 1, 80), (1, 2, 96), (1, 3, 70),
    (2, 1, 55), (2, 2, 61),
    (3, 1, 90), (3, 2, 72), (3, 3, 88);
