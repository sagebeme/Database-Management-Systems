-- Keep only the first sign-up (lowest id) for each address, store every email trimmed and lower-case, then
-- make email unique so it can't happen again.
-- Write your statement below this line.
DELETE s FROM signups AS s
JOIN signups AS first ON LOWER(TRIM(first.email)) = LOWER(TRIM(s.email)) AND first.id < s.id;
UPDATE signups SET email = LOWER(TRIM(email));
ALTER TABLE signups ADD UNIQUE (email);
