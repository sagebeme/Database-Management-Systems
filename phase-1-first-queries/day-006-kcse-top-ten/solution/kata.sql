-- Kata: Runner-Up Score. The second-highest number of points anyone got, in a column called second_best.
SELECT DISTINCT points AS second_best FROM results ORDER BY points DESC LIMIT 1 OFFSET 1;
