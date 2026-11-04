-- Each county and the hottest reading it had (hottest), alphabetical by county.
SELECT county, MAX(max_c) AS hottest FROM readings GROUP BY county ORDER BY county;
