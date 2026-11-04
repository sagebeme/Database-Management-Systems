-- number and destination of every route whose destination mentions Rongai in any mix of capitals,
-- by number.
-- Write your statement below this line.
SELECT number, destination FROM routes WHERE destination ILIKE '%rongai%' ORDER BY number;
