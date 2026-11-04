-- A CHECK constraint, phone_shape, using JSON_SCHEMA_VALID: a phone's attributes must have ram_gb and
-- storage_gb, both whole numbers from 0 up. Other categories can hold anything.
-- Write your statement below this line.
ALTER TABLE products ADD CONSTRAINT phone_shape CHECK (
    category <> 'phone' OR JSON_SCHEMA_VALID('{
        "type": "object",
        "required": ["ram_gb", "storage_gb"],
        "properties": {
            "ram_gb": {"type": "integer", "minimum": 0},
            "storage_gb": {"type": "integer", "minimum": 0}
        }
    }', attributes)
);
