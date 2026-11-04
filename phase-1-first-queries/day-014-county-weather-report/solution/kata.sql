-- Kata: Coldest Night. The single coldest reading of the year: county, recorded_on and min_c.
SELECT county, recorded_on, min_c FROM readings ORDER BY min_c LIMIT 1;
