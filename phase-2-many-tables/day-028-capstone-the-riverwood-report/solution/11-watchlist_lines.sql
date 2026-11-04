-- One line per viewer, alphabetical, listing what they saved (the show title, or the requested title when Riverwood lacks it), alphabetical: like 'akinyi: Nairobi Nights, Siri za Lamu'.
-- Columns: line
SELECT CONCAT(w.viewer, ': ', GROUP_CONCAT(COALESCE(s.title, w.requested_title)
                                       ORDER BY COALESCE(s.title, w.requested_title) SEPARATOR ', ')) AS line
FROM watchlist AS w
LEFT JOIN tv_shows AS s ON s.id = w.show_id
GROUP BY w.viewer
ORDER BY w.viewer;
