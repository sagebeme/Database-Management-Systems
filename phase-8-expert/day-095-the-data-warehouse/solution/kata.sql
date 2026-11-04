-- Kata: a slowly changing dimension, type 2. Some shops in the shop system have changed name or county. For each
-- shop whose current dim_shop row no longer matches it: close that row (valid_to = CURRENT_DATE - 1, not current)
-- and add a new current row valid from CURRENT_DATE. Shops that haven't changed are left alone, so running it
-- twice changes nothing the second time. Old facts keep pointing at the old row.
WITH changed AS (
    UPDATE dim_shop AS d
    SET valid_to = CURRENT_DATE - 1, is_current = false
    FROM shops AS s
    WHERE d.shop_id = s.id AND d.is_current AND (d.name, d.county) IS DISTINCT FROM (s.name, s.county)
    RETURNING s.id, s.name, s.county
)
INSERT INTO dim_shop (shop_id, name, county, valid_from, valid_to, is_current)
SELECT id, name, county, CURRENT_DATE, NULL, true FROM changed;
