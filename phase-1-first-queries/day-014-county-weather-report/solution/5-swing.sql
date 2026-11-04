-- Each county's swing: its hottest high minus its coldest low (swing), biggest first, ties alphabetical.
SELECT county, MAX(max_c) - MIN(min_c) AS swing
FROM readings
GROUP BY county
ORDER BY swing DESC, county;
