-- Add an optional email column (VARCHAR(100)) to subscribers, right after name.
ALTER TABLE subscribers ADD COLUMN email VARCHAR(100) NULL AFTER name;
