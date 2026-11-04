-- Kata: Room for Long Names. Widen subscribers.name to VARCHAR(100). It must stay required.
ALTER TABLE subscribers MODIFY name VARCHAR(100) NOT NULL;
