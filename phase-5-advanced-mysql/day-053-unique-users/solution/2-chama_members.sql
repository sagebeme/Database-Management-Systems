-- chama_members, with every rule in the README's table:
--   id, chama_id, name, phone, born_on, role, monthly_contribution
-- Write your statement below this line.
DROP TABLE IF EXISTS chama_members;
CREATE TABLE chama_members (
    id INT AUTO_INCREMENT PRIMARY KEY,
    chama_id INT NOT NULL,
    name VARCHAR(60) NOT NULL,
    phone CHAR(12) NOT NULL UNIQUE,
    born_on DATE NOT NULL,
    role ENUM('member', 'treasurer', 'secretary', 'chair') NOT NULL DEFAULT 'member',
    monthly_contribution INT NOT NULL,
    UNIQUE (chama_id, name),
    CHECK (phone REGEXP '^254[17][0-9]{8}$'),
    CHECK (born_on >= '1900-01-01'),
    CHECK (monthly_contribution BETWEEN 100 AND 100000)
);
