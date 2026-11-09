-- Clue 4. Who else was there: every username that logged in successfully from an IP address a ghost login (Clue 3)
-- came from, leaving out the accounts of people who have left. Each username once, alphabetical.
SELECT DISTINCT l.username
FROM logins AS l
WHERE l.success
  AND l.ip IN (
      SELECT g.ip
      FROM logins AS g
      JOIN staff AS s ON s.username = g.username
      WHERE g.success AND DATE(g.at) > s.left_on
  )
  AND l.username NOT IN (SELECT username FROM staff WHERE left_on IS NOT NULL)
ORDER BY l.username;
