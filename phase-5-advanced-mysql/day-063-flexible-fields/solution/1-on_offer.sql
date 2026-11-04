-- Every product under 500 shillings gets "on_offer": true in its attributes. Nothing else changes.
-- Write your statement below this line.
UPDATE products
SET attributes = JSON_SET(attributes, '$.on_offer', TRUE)
WHERE price < 500;
