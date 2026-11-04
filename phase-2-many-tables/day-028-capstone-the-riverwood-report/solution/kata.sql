-- Kata: Twins. Pairs of different shows with exactly the same set of genres (at least one): show_a, show_b, show_a alphabetically before show_b. Ordered by show_a, then show_b.
-- Columns: show_a, show_b
SELECT a.title AS show_a, b.title AS show_b
FROM (SELECT s.title, GROUP_CONCAT(sg.genre_id ORDER BY sg.genre_id) AS genre_set
      FROM tv_shows AS s JOIN tv_show_genres AS sg ON sg.show_id = s.id
      GROUP BY s.id, s.title) AS a
JOIN (SELECT s.title, GROUP_CONCAT(sg.genre_id ORDER BY sg.genre_id) AS genre_set
      FROM tv_shows AS s JOIN tv_show_genres AS sg ON sg.show_id = s.id
      GROUP BY s.id, s.title) AS b
  ON a.genre_set = b.genre_set AND a.title < b.title
ORDER BY show_a, show_b;
