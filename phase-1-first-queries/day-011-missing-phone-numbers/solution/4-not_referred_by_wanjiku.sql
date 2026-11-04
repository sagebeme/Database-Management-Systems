-- Names of every customer not referred by Wanjiku (id 1), including those nobody referred. Alphabetical.
SELECT name FROM customers
WHERE referred_by <> 1 OR referred_by IS NULL
ORDER BY name;
