-- An index, idx_name_first_score, on the first letter of names.name and then score.
-- Write your statement below this line.
CREATE INDEX idx_name_first_score ON names (name(1), score);
