-- A schema called reports, and in it a view route_fares: number, sacco (the sacco's name), fare, for every
-- route.
-- Write your statement below this line.
CREATE SCHEMA reports;
CREATE VIEW reports.route_fares AS
SELECT r.number, s.name AS sacco, r.fare
FROM routes AS r
JOIN saccos AS s ON s.id = r.sacco_id;
