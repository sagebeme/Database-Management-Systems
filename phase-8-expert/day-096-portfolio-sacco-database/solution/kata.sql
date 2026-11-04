-- Day 96 kata: dividends on savings held at the end of a year.

CREATE FUNCTION dividends(p_year integer, p_rate numeric)
RETURNS TABLE (member_id integer, name text, dividend bigint)
LANGUAGE sql STABLE AS $$
    SELECT m.id, m.name, floor(s.held * p_rate / 100)::bigint
    FROM members m
    JOIN LATERAL (
        SELECT COALESCE(sum(CASE kind WHEN 'deposit' THEN amount ELSE -amount END), 0) AS held
        FROM ledger l
        WHERE l.member_id = m.id AND l.at < make_date(p_year + 1, 1, 1)
    ) s ON s.held > 0
    ORDER BY m.id;
$$;
