-- Day 96: what the treasurer reads.

CREATE VIEW member_summary AS
SELECT m.id AS member_id, m.name,
       savings(m.id) AS savings,
       COALESCE((SELECT balance FROM loans l WHERE l.member_id = m.id AND l.status = 'active'), 0) AS loan_balance,
       guaranteed(m.id) AS guaranteed,
       free_savings(m.id) AS free_savings
FROM members m;

CREATE VIEW monthly_flows AS
SELECT to_char(date_trunc('month', at), 'YYYY-MM') AS month,
       COALESCE(sum(amount) FILTER (WHERE kind = 'deposit'), 0) AS deposits,
       COALESCE(sum(amount) FILTER (WHERE kind = 'withdrawal'), 0) AS withdrawals
FROM ledger
GROUP BY 1;
