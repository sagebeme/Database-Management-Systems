-- An index, idx_name_first, on the first letter of names.name.
-- Write your statement below this line.
CREATE INDEX idx_name_first ON names (name(1));
