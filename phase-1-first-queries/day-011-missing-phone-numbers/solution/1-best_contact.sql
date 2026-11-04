-- Every customer's name and one way to reach them (contact): their phone, else their email, else the words no contact. Alphabetical.
SELECT name, COALESCE(phone, email, 'no contact') AS contact FROM customers ORDER BY name;
