# Day 13: Majina na Emoji

## The brief

Wanjiru's wedding planner in Nyeri keeps the guest list in a MySQL table that a cousin made years ago. Two problems turned up this week. A guest's name with an emoji in it, the way she writes it on WhatsApp, was rejected with `Incorrect string value`. And a search for "Renee" missed "Renée".

Both come down to how the database stores text. Today you look at the table's **character set** (which characters it can store) and **collation** (how it compares and sorts them), move it to the modern standard, and use collations on purpose.

## What you'll use

**Character sets.** Text is stored as bytes, and a character set is the code that maps characters to bytes.

- `latin1` uses one byte per character and knows about 256 characters: English letters plus Western European ones like é. No emoji, no Amharic, no Arabic.
- `utf8mb4` is UTF-8: every character in Unicode, using 1 to 4 bytes each. Plain English letters take 1 byte, é takes 2, 🌻 takes 4. **Use it for everything.** It's MySQL 8's default.
- MySQL's older `utf8` (also called `utf8mb3`) stops at 3 bytes, so it can't store emoji. The name is a trap: always write `utf8mb4`.

**Collations** decide what counts as equal and how text sorts. The name says how:

| Collation | Meaning |
|---|---|
| `utf8mb4_0900_ai_ci` | MySQL 8's default: **a**ccent-**i**nsensitive, **c**ase-**i**nsensitive (`Renée` = `renee`) |
| `utf8mb4_unicode_ci` | older Unicode rules, also case- and accent-insensitive |
| `utf8mb4_0900_as_cs` | accent- and case-sensitive |
| `utf8mb4_bin` | compares the raw codes: `AMINA` ≠ `Amina` |

You can override the collation for one comparison: `WHERE name LIKE 'AMINA%' COLLATE utf8mb4_bin`.

**Changing an existing table:**

```sql
ALTER DATABASE CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;   -- the default for NEW tables (no name = current database)
ALTER TABLE guests CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;   -- converts the data too
```

`ALTER DATABASE` only changes the default for tables created later. Existing tables need `CONVERT TO`, which rewrites every text column and keeps the characters (é stays é).

**Length**: `CHAR_LENGTH` counts characters, `LENGTH` counts bytes. In `utf8mb4` they differ as soon as a name has an accent or an emoji. `VARCHAR(60)` means 60 *characters*.

## Steps

```bash
tools/mysql.sh -e "CREATE DATABASE IF NOT EXISTS harusi;"
tools/mysql.sh harusi < phase-1-first-queries/day-013-majina-na-emoji/setup.sql
```

1. `starter/0-show_charsets.sql`: for each column of `guests`, its `column_name`, `character_set_name` and `collation_name` from `information_schema.columns`, in column order.
2. `starter/1-move_to_utf8mb4.sql`: make `utf8mb4` / `utf8mb4_unicode_ci` the current database's default, and convert `guests` to it.
3. `starter/2-add_emoji_guest.sql`: add guest `7`, `Zawadi 🌻`, side `bride`. (It fails before step 2 and works after.)
4. `starter/3-chars_and_bytes.sql`: each `name` with `chars` and `bytes`, in id order.
5. `starter/4-renee_search.sql`: names starting with "Renee", whatever the case and accents, in id order.
6. `pytest phase-1-first-queries/day-013-majina-na-emoji`

Save your files as UTF-8 (every modern editor does), or the 🌻 in step 3 arrives mangled.

## The kata: Shouting Names

In `starter/kata.sql`, list the names that start with `AMINA` in capitals exactly, in id order. The table's collation says `Amina` and `AMINA` are equal, so you'll need to override it.

## When you're stuck

- **`Incorrect string value: '\xF0\x9F\x8C\xBB'`**: the column is still `latin1` (or `utf8mb3`). Convert it.
- **The table test passes but the database test fails**: `ALTER TABLE` changes the table; the database default needs `ALTER DATABASE` too.
- **`Renée` comes out as `RenÃ©e`**: the text went in as one character set and was read as another. Here, check your editor saves UTF-8.
- **The search finds only Renee**: the column's collation is accent-sensitive. Make sure step 2 converted it.
- **The kata returns both Aminas**: add `COLLATE utf8mb4_bin` to the comparison.
