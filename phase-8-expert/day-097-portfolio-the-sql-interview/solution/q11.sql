WITH earnings AS (
    SELECT d.county, d.name AS driver, sum(t.fare) AS earnings,
           rank() OVER (PARTITION BY d.county ORDER BY sum(t.fare) DESC) AS r
    FROM drivers d JOIN trips t ON t.driver_id = d.id AND t.status = 'completed'
    GROUP BY d.county, d.id, d.name
)
SELECT county, driver, earnings FROM earnings WHERE r = 1 ORDER BY county, driver;
