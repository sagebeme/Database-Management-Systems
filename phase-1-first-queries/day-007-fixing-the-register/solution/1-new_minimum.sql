-- Everyone paying 500 a month now pays 600.
UPDATE members SET monthly_contribution = 600 WHERE monthly_contribution = 500;
