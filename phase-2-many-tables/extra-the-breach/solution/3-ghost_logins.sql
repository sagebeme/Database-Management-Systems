-- Clue 3. Ghost logins: every successful login by an account whose owner had already left (after their last day,
-- left_on): username, ip, at, oldest first.
SELECT l.username, l.ip, l.at
FROM logins AS l
JOIN staff AS s ON s.username = l.username
WHERE l.success AND DATE(l.at) > s.left_on
ORDER BY l.at;
