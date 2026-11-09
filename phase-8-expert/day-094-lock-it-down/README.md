# Day 94: Lock It Down

## The brief

Kenya's Data Protection Act 2019 makes a SACCO answerable for who sees its members' phone numbers and ID numbers. A teller needs names to serve people, not ID numbers. One loan officer has no business reading another's loans. And when a loan amount changes, the SACCO must be able to say who changed it, from what, and when, with a record nobody can quietly edit.

Most data leaks aren't clever hacks: they're an app that connects as a superuser, or a staff account that can read everything. Today you'll lock down a SACCO's database in Postgres with **roles**, **grants** down to single columns, **row-level security**, and a tamper-resistant **audit trail**. And when members log in to the SACCO's app, you'll store their passwords the only safe way: **not at all**.

## What you'll use

**Roles** are users and groups at once. They belong to the whole server, not to one database.

```sql
CREATE ROLE sacco_teller LOGIN;          -- can connect; add PASSWORD '...' for a real one
```

**Least privilege**: a new role can do almost nothing. Grant exactly what the job needs:

```sql
GRANT SELECT (id, name) ON members TO sacco_teller;    -- only these columns
GRANT SELECT, INSERT ON loans TO sacco_teller;
REVOKE ... FROM ...;
```

The table's owner (here `postgres`) can do everything, and a superuser skips every check. Apps should never connect as either.

**Row-level security (RLS)** filters *rows* by who's asking:

```sql
ALTER TABLE loans ENABLE ROW LEVEL SECURITY;           -- now roles see no rows unless a policy allows them
CREATE POLICY own_loans ON loans TO sacco_teller
    USING (officer = current_user)                     -- which rows they can see (and update or delete)
    WITH CHECK (officer = current_user);               -- which rows they can add or change them into
```

Policies are added together: a role sees a row if any of its policies allow it. The table owner isn't affected (unless you `FORCE ROW LEVEL SECURITY`).

**Auditing with a trigger**: `AFTER INSERT OR UPDATE OR DELETE ... FOR EACH ROW`, with `TG_OP` (`'INSERT'`, `'UPDATE'`, `'DELETE'`), `OLD` and `NEW`, and `to_jsonb(OLD)` to keep the whole row.

The teller has no rights on `audit_log`, so how does their change get logged? A function marked **`SECURITY DEFINER`** runs with the rights of its *owner*, like a setuid program. Inside it, `current_user` is the owner; `session_user` is who actually logged in. Pin its `search_path` (`SET search_path = public`) so nobody can trick it into using their own table of the same name.

**Append-only**: grants alone can't stop the owner. A `BEFORE UPDATE OR DELETE` trigger that raises an exception stops everyone except someone who drops the trigger, and dropping it is itself something you can watch for.

**Passwords: store a hash, never the password.** If the database leaks (and Extra: The Breach shows how easily it can), a table of passwords hands an attacker every account. People reuse passwords, so it also hands over their M-Pesa and email. Store a **hash** instead: a scrambled fingerprint of the password that can't be turned back into it. To log someone in, hash what they typed and compare the two.

Not just any hash. `md5` and `sha256` are built to be *fast*, so a stolen table can be guessed at billions of tries a second. A password hash is built to be *slow*. **bcrypt** is the classic one; **argon2** is the newer choice. Each also mixes in a random **salt**, so two people with the same password get different hashes, and one guess can't test everyone at once. Postgres has bcrypt in the `pgcrypto` extension:

```sql
CREATE EXTENSION IF NOT EXISTS pgcrypto;
SELECT crypt('mpesa2026', gen_salt('bf', 10));         -- $2a$10$...: bcrypt, cost 10 (2^10 rounds), salt built in
SELECT stored = crypt('what they typed', stored);       -- check: the salt and cost are read back out of the stored hash
```

Raise the cost as computers get faster: each step up doubles the work.

In a real app, hash in the **app**, not in SQL: `bcrypt` or `argon2-cffi` in Python (Day 81). Then the plain password never travels to the database, where it can end up in the query log. Doing it in SQL here shows exactly what's stored.

One more Postgres surprise: **every new function can be run by everyone** (`PUBLIC`) until you `REVOKE EXECUTE ... FROM PUBLIC`.

## Steps

```bash
tools/psql.sh postgres -c "CREATE DATABASE locked;"
tools/psql.sh locked -f phase-8-expert/day-094-lock-it-down/setup.sql
```

1. `starter/0-roles.sql`, then `starter/1-grants.sql`. Test them: `tools/psql.sh locked -U sacco_teller` and try to read a phone number.
2. `starter/2-row_security.sql`.
3. `starter/3-audit.sql`.
4. `starter/4-passwords.sql`. Try it: `SELECT set_password(1, 'mpesa2026');`, then `SELECT * FROM member_logins;`, and run it again to see a different hash.
5. `pytest phase-8-expert/day-094-lock-it-down`

The tests log in as each role and try things they shouldn't be able to do.

## The kata: Nobody Edits History

In `starter/kata.sql`, make `audit_log` append-only for everyone, its owner included: no `UPDATE`, no `DELETE`, no `TRUNCATE`.

## When you're stuck

- **`role "sacco_teller" already exists`**: roles outlive databases. `DROP ROLE sacco_teller;` (after dropping what it owns) and start again. The tests clean up after themselves.
- **The teller can still read phone numbers**: check you didn't also `GRANT SELECT ON members` (the whole table) somewhere. Look with `\dp members`.
- **The teller sees no loans at all**: enabling RLS hides every row until a policy allows some. Check the policy is `TO` the right roles.
- **The teller can file a loan under `sacco_teller2`**: `USING` only filters what they see; `WITH CHECK` is what stops them writing such rows.
- **`permission denied for table audit_log`** when a teller adds a loan: the trigger function runs as the teller. Make it `SECURITY DEFINER`.
- **Every audit row says `postgres`**: inside a `SECURITY DEFINER` function, `current_user` is the owner. Use `session_user`.
- **`function gen_salt(unknown) does not exist`**: run `CREATE EXTENSION IF NOT EXISTS pgcrypto;` first, in this database.
- **Both members' hashes are the same**: you salted with a fixed string. `gen_salt('bf', 10)` makes a new salt every call.
- **`check_password` returns `NULL` for a member with no password**: the subquery found no row. Wrap it in `coalesce(..., false)`.
- **A teller can call `set_password`**: functions start out runnable by everyone. `REVOKE EXECUTE ON FUNCTION ... FROM PUBLIC`, then grant `check_password` to the tellers only.
- **`TRUNCATE audit_log` still works**: row triggers don't fire on `TRUNCATE`. It needs a `BEFORE TRUNCATE ... FOR EACH STATEMENT` trigger of its own.
