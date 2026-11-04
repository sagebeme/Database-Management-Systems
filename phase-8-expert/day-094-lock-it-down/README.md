# Day 94: Lock It Down

## The brief

Kenya's Data Protection Act 2019 makes a SACCO answerable for who sees its members' phone numbers and ID numbers. A teller needs names to serve people, not ID numbers. One loan officer has no business reading another's loans. And when a loan amount changes, the SACCO must be able to say who changed it, from what, and when, with a record nobody can quietly edit.

Most data leaks aren't clever hacks: they're an app that connects as a superuser, or a staff account that can read everything. Today you'll lock down a SACCO's database in Postgres with **roles**, **grants** down to single columns, **row-level security**, and a tamper-resistant **audit trail**.

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

## Steps

```bash
tools/psql.sh postgres -c "CREATE DATABASE locked;"
tools/psql.sh locked -f phase-8-expert/day-094-lock-it-down/setup.sql
```

1. `starter/0-roles.sql`, then `starter/1-grants.sql`. Test them: `tools/psql.sh locked -U sacco_teller` and try to read a phone number.
2. `starter/2-row_security.sql`.
3. `starter/3-audit.sql`.
4. `pytest phase-8-expert/day-094-lock-it-down`

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
- **`TRUNCATE audit_log` still works**: row triggers don't fire on `TRUNCATE`. It needs a `BEFORE TRUNCATE ... FOR EACH STATEMENT` trigger of its own.
