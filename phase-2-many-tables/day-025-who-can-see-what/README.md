# Day 25: Who Can See What

## The brief

So far you've used one MySQL account, `root`, which can do anything to anything. Riverwood Plus is about to have several programs and people touching its data: the website only needs to read the catalogue, the payments service writes payouts, and the finance team reads reports. If the website's password leaks, the damage should stop at what the website was allowed to do.

That's the **principle of least privilege**: give every account exactly the access its job needs, and nothing more. Today you create accounts, grant and take away privileges, check who has what, and change a leaked password.

## What you'll use

A MySQL account is a **user name and a host**: `'rw_app'@'localhost'` (connecting from this machine) and `'rw_app'@'%'` (from anywhere) are two different accounts. Today's accounts use `'%'`.

```sql
CREATE USER IF NOT EXISTS 'name'@'%' IDENTIFIED BY 'password';
GRANT SELECT, INSERT ON shop.* TO 'name'@'%';    -- these privileges, every table in shop
GRANT ALL PRIVILEGES ON *.* TO 'name'@'%';       -- everything, everywhere: root in all but name
REVOKE INSERT ON shop.* FROM 'name'@'%';         -- take one back
SHOW GRANTS FOR 'name'@'%';                      -- what does this account have?
ALTER USER 'name'@'%' IDENTIFIED BY 'new';       -- change the password
DROP USER IF EXISTS 'name'@'%';
```

| Privilege | Lets the account |
|---|---|
| `SELECT` | read rows |
| `INSERT`, `UPDATE`, `DELETE` | add, change, remove rows |
| `CREATE`, `ALTER`, `DROP` | make, reshape, remove tables and databases |
| `ALL PRIVILEGES` | all of the above and more |

- **`ON` sets how far the grant reaches**: `*.*` is every database, `shop.*` every table in `shop`, `shop.orders` one table.
- **A grant on a database that doesn't exist yet is allowed.** It applies once the database is created. That's why order doesn't matter much in setup scripts.
- **Privileges add up.** `REVOKE` takes away exactly what you name; the rest stays.
- **Log in as the account to check it**: `tools/mysql.sh -urw_reader -p`. The tests do exactly this.

The passwords today (`rw_reader_dev` and the like) are made-up practice values. A real password never goes in a `.sql` file you commit: it lives in a password manager or a gitignored `.env`, the same rule as the course's own `.env`.

## Steps

These tasks change server-wide accounts, so practise on your course server, not on a server other people use. The tests create and remove `rw_admin`, `rw_reader`, `rw_app` and `riverwood_ops` themselves.

1. `starter/0-create_admin.sql`: create `rw_admin` (any host, password `rw_admin_dev`) if missing, with all privileges on everything. (Then notice how much that is.)
2. `starter/1-create_reader.sql`: create the database `riverwood_ops` and the user `rw_reader` (password `rw_reader_dev`), both only if missing. `rw_reader` may read `riverwood_ops` and nothing else.
3. `starter/2-show_grants.sql`: show `rw_admin`'s privileges, then `rw_reader`'s.
4. `starter/3-create_app_user.sql`: create `rw_app` (password `rw_app_dev`) if missing. In `riverwood_ops` it may read, insert and update rows, but not delete.
5. `starter/4-revoke_insert.sql`: `rw_app` must stop inserting into `riverwood_ops`. Take away only that.
6. `pytest phase-2-many-tables/day-025-who-can-see-what`

## The kata: Change the Locks

In `starter/kata.sql`, `rw_reader`'s password has leaked. Change it to `rw_reader_new` without touching its privileges.

## When you're stuck

- **`ERROR 1396: Operation CREATE USER failed`**: the account already exists. Use `CREATE USER IF NOT EXISTS`.
- **`ERROR 1045: Access denied for user 'rw_reader'`** when you log in: the password is wrong, or you made the account at a different host. `SELECT user, host FROM mysql.user;` lists them.
- **`ERROR 1141: There is no such grant defined`**: `SHOW GRANTS` and `REVOKE` must name the same `'user'@'host'` you created.
- **The reader can see other databases**: you granted on `*.*`. Grant on `riverwood_ops.*`.
- **The app can't update after the revoke**: you revoked more than `INSERT`, or ran `REVOKE ALL`.
