-- Kata: Suspensions. Active members owing more than 1,000 bob become suspended.
UPDATE members SET status = 'suspended' WHERE status = 'active' AND arrears_kes > 1000;
