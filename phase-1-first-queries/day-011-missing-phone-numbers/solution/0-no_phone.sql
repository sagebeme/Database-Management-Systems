-- Names of customers with no phone number, alphabetical.
SELECT name FROM customers WHERE phone IS NULL ORDER BY name;
