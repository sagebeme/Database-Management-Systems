-- Clue 5. Resets nobody asked for: every password reset with no help-desk ticket: account, reset_by, at,
-- oldest first.
SELECT account, reset_by, at
FROM password_resets
WHERE ticket_id IS NULL
ORDER BY at;
