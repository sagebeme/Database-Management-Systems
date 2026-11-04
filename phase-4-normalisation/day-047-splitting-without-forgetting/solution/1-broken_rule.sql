-- The rule (street, town) -> zone was lost in the split. Find where it's broken: street, town, zones (how many),
-- for each street and town with more than one zone. By street.
SELECT a.street, z.town, COUNT(*) AS zones
FROM addresses AS a
JOIN zones AS z ON z.zone = a.zone
GROUP BY a.street, z.town
HAVING COUNT(*) > 1
ORDER BY a.street;
