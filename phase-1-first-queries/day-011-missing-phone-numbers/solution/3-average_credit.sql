-- Two averages of credit_limit, rounded to 2 places: avg_known (ignoring unknown limits) and avg_unknown_as_zero.
SELECT ROUND(AVG(credit_limit), 2) AS avg_known,
       ROUND(AVG(COALESCE(credit_limit, 0)), 2) AS avg_unknown_as_zero
FROM customers;
