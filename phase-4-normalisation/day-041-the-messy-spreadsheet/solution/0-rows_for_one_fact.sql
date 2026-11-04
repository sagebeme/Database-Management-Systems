-- How many rows record which room Mr Omondi teaches in? Column: rows.
SELECT COUNT(*) AS `rows` FROM registrations_flat WHERE tutor = 'Mr Omondi';
