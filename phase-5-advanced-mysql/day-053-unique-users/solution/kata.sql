-- One chair per chama: change chama_members so a second chair in the same chama is refused. Any number of
-- members, treasurers and secretaries is still fine.
-- Write your statement below this line.
ALTER TABLE chama_members
    ADD UNIQUE INDEX one_chair_per_chama ((CASE WHEN role = 'chair' THEN chama_id END));
