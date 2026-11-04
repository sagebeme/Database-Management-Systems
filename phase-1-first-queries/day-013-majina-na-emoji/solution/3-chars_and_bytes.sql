-- Each guest's name with its length in characters (chars) and in bytes (bytes), in id order.
SELECT name, CHAR_LENGTH(name) AS chars, LENGTH(name) AS bytes FROM guests ORDER BY id;
