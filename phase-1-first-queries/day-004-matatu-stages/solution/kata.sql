-- Kata: Shillings per Kilometre. Route number and fare per km (rounded to 2 places) of routes dearer than 5 bob a km.
SELECT route_no, ROUND(fare_kes / distance_km, 2) AS per_km
FROM routes
WHERE fare_kes / distance_km > 5;
