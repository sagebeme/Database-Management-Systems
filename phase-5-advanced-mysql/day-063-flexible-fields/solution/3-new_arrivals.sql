-- Products tagged "new": name, category. Alphabetical by name.
-- Write your statement below this line.
SELECT name, category
FROM products
WHERE 'new' MEMBER OF (attributes->'$.tags')
ORDER BY name;
