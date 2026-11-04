SELECT (SELECT DISTINCT fare FROM trips WHERE status = 'completed'
        ORDER BY fare DESC OFFSET 1 LIMIT 1) AS second_highest;
