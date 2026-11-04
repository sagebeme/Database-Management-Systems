-- One line per county, alphabetical, in a column called line, like: Kakamega: 2,102.6 mm of rain in 2024
SELECT CONCAT(county, ': ', FORMAT(SUM(rain_mm), 1), ' mm of rain in 2024') AS line
FROM readings
GROUP BY county
ORDER BY county;
