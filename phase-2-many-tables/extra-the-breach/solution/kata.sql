-- Kata: Close the Door. One UPDATE that disables the account of everyone who has left, and nobody else's.
UPDATE staff
SET account_enabled = FALSE
WHERE left_on IS NOT NULL;
