-- The two biggest artists in each genre (equal fans: alphabetical first): genre, name, fans.
-- By genre, then fans (most first), then name.
-- Write your statement below this line.
SELECT genre, name, fans
FROM (
    SELECT genre, name, fans, ROW_NUMBER() OVER (PARTITION BY genre ORDER BY fans DESC, name) AS n
    FROM artists
) AS ranked
WHERE n <= 2
ORDER BY genre, fans DESC, name;
