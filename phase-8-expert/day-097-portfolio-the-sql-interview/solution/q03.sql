SELECT phone, count(*) AS riders
FROM riders
GROUP BY phone
HAVING count(*) > 1
ORDER BY phone;
