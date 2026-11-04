-- Rename subscribers.phone to msisdn, keeping its type and data.
ALTER TABLE subscribers RENAME COLUMN phone TO msisdn;
