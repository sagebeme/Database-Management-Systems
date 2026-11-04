-- Members in Kakamega increase their monthly contribution by 10%.
UPDATE members SET monthly_contribution = monthly_contribution * 1.10 WHERE county = 'Kakamega';
