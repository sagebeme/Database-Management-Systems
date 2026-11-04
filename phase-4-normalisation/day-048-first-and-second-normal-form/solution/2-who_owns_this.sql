-- Who owns 254744000003? name.
SELECT m.name
FROM members_raw AS m
JOIN member_phones AS p ON p.member_id = m.id
WHERE p.phone = '254744000003';
