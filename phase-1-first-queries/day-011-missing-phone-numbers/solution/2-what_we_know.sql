-- Three counts in one row: customers, with_phone, with_email.
SELECT COUNT(*) AS customers, COUNT(phone) AS with_phone, COUNT(email) AS with_email FROM customers;
