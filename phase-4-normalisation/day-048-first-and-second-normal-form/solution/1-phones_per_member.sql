-- Every member and how many phones they have, zero included: name, phones. Most first, ties alphabetical.
SELECT m.name, COUNT(p.phone) AS phones
FROM members_raw AS m
LEFT JOIN member_phones AS p ON p.member_id = m.id
GROUP BY m.id, m.name
ORDER BY phones DESC, m.name;
