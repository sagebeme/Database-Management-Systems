-- Kata: Name the Rule. Add phone (CHAR(12), optional) to riders, with a CHECK constraint called phone_format:
-- a phone, when given, is 2547 or 2541 followed by 8 digits.
ALTER TABLE riders
    ADD COLUMN phone CHAR(12) NULL,
    ADD CONSTRAINT phone_format CHECK (phone REGEXP '^254[71][0-9]{8}$');
