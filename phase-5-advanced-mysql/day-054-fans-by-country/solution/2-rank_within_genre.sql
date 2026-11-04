-- Each artist's rank inside their genre by fans, with no gaps after a tie: genre, name, fans, genre_rank.
-- By genre, then genre_rank, then name.
-- Write your statement below this line.
SELECT genre, name, fans, DENSE_RANK() OVER (PARTITION BY genre ORDER BY fans DESC) AS genre_rank
FROM artists
ORDER BY genre, genre_rank, name;
