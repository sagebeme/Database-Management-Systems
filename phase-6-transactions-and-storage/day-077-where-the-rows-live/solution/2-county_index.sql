-- An index called idx_county_savings that lets MySQL answer
--     SELECT county, COUNT(*) AS members, SUM(savings) AS savings FROM members GROUP BY county;
-- from the index alone.
-- Write your statement below this line.
CREATE INDEX idx_county_savings ON members (county, savings);
