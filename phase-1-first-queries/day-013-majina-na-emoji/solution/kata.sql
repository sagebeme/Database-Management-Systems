-- Kata: Shouting Names. Names of guests whose name starts with AMINA in capital letters exactly. In id order.
SELECT name FROM guests WHERE name LIKE 'AMINA%' COLLATE utf8mb4_bin ORDER BY id;
