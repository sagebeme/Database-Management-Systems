-- Every subscriber must have a plan, 'basic' unless told otherwise. Give the blank ones 'basic' first.
UPDATE subscribers SET plan = 'basic' WHERE plan IS NULL;
ALTER TABLE subscribers MODIFY plan VARCHAR(10) NOT NULL DEFAULT 'basic';
