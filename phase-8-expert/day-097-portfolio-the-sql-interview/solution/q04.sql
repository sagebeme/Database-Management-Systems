SELECT r.id, r.name
FROM riders r
WHERE NOT EXISTS (SELECT 1 FROM trips t WHERE t.rider_id = r.id AND t.status = 'completed')
ORDER BY r.id;
