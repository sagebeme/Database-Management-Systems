-- A generated column, ram_gb (INT), worked out from the JSON (NULL for products without one), and an index on
-- it, idx_ram_gb.
-- Write your statement below this line.
ALTER TABLE products
    ADD COLUMN ram_gb INT GENERATED ALWAYS AS (attributes->>'$.ram_gb') VIRTUAL,
    ADD INDEX idx_ram_gb (ram_gb);
