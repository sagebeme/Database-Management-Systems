-- Kisumu (county id 6) is leaving the list. Delete it, along with its towns: the order of your statements matters.
DELETE FROM towns WHERE county_id = 6;
DELETE FROM counties WHERE id = 6;
