-- The id and phone of the member whose phone is 254700007919. With uq_phone in place, MySQL should answer this
-- from the index alone, without touching the table's rows.
-- Write your statement below this line.
SELECT id, phone FROM members WHERE phone = '254700007919';
