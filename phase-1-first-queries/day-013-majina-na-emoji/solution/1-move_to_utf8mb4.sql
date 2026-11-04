-- Make utf8mb4 with the utf8mb4_unicode_ci collation the default for the current database, and convert the guests table to it.
ALTER DATABASE CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
ALTER TABLE guests CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
