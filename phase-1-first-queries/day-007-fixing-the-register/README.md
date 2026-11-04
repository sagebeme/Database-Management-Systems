# Day 7: Fixing the Register

## The brief

The Umoja Women's Group's register has been typed in, and Mama Atieno has found mistakes. One phone number is missing a digit. The group has voted to raise the minimum contribution. Two members have left. One has moved. And members far behind on payments are to be suspended until they catch up.

Today you change rows that are already there with **`UPDATE`**, and remove them with **`DELETE`**. These are the two most dangerous statements in SQL, because one missing line changes every row in the table, so today is also about doing them safely.

## What you'll use

```sql
UPDATE members SET phone = '254712000999' WHERE id = 3;
UPDATE members SET county = 'Busia', phone = '254700000003' WHERE id = 3;   -- two columns at once
UPDATE members SET monthly_contribution = monthly_contribution + 100 WHERE county = 'Vihiga';
DELETE FROM members WHERE status = 'left';
```

**The safe way to change data:**

1. Write the `WHERE` first, as a `SELECT`, and look at what it finds:

   ```sql
   SELECT * FROM members WHERE status = 'left';
   ```

2. When those are exactly the rows you mean, change `SELECT *` to `DELETE` (or `UPDATE ... SET ...`) and keep the same `WHERE`.
3. MySQL tells you how many rows it touched: `Query OK, 2 rows affected`. If that number surprises you, stop.

**Without `WHERE`, every row changes.** `UPDATE members SET phone = '254712000104';` gives all eight members the same phone number. There's no undo button: the only way back is a backup, or a transaction you haven't committed yet (Day 65). At the `mysql>` prompt you can make MySQL refuse these by turning on safe-updates mode:

```sql
SET sql_safe_updates = 1;
```

Then an `UPDATE` or `DELETE` without a `WHERE` on a key column is rejected.

`SET` can use the old value: `SET monthly_contribution = monthly_contribution * 1.10` raises each row by 10% of *its own* amount.

## Steps

```bash
tools/mysql.sh -e "CREATE DATABASE IF NOT EXISTS chama;"
tools/mysql.sh chama < phase-1-first-queries/day-007-fixing-the-register/setup.sql
```

Run `setup.sql` again any time to get the original, mistake-filled register back. Each test starts from it too.

1. `starter/0-fix_phone.sql`: Makokha Juma (id 4)'s number is `254712000104`.
2. `starter/1-new_minimum.sql`: everyone paying 500 a month now pays 600.
3. `starter/2-kakamega_raise.sql`: members in Kakamega raise their contribution by 10%.
4. `starter/3-remove_leavers.sql`: remove members whose status is `left`.
5. `starter/4-moved.sql`: Khaemba Simiyu (id 7) is now in Bungoma, on `254733000107`. One `UPDATE`.
6. `pytest phase-1-first-queries/day-007-fixing-the-register`

The tests look at the whole table afterwards, so they also catch rows that changed when they shouldn't have.

## The kata: Suspensions

In `starter/kata.sql`, set `status` to `'suspended'` for active members who owe (`arrears_kes`) more than 1,000 bob. Members who have left stay `left`.

## When you're stuck

- **The test shows every row changed**: your `WHERE` is missing or always true.
- **Use `id` to pick one row**, not the name: two members can share a name, but not an id. (Day 16 makes the database promise that.)
- **`ERROR 1175: You are using safe update mode`**: your `WHERE` doesn't use a key column. Fine at the prompt; here, run with safe updates off, or add a key to the condition.
- **The 10% raise gives 550.0000**: it won't in this table, because `DECIMAL(8, 2)` keeps two decimal places and rounds the rest.
- **The moved member needs two statements**: separate the columns with a comma: `SET county = ..., phone = ...`.
