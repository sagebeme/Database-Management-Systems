# Extra: The Breach

This case sits after Day 28, outside the hundred days. Do it at the end of Phase 2: it uses nothing you haven't met yet, just all of it at once.

## The brief

On the morning of 14 October, someone posts a file for sale on a forum: 5,000 names and phone numbers, the whole customer list of **Soko Safi**, an online grocer in Nairobi. Nobody outside the company should have that list. The managing director gives you read access to the staff system's logs and one question: **who did it?**

You won't find a confession in the data. You'll find a trail: an export, an account that should have been dead, an IP address that shows up twice, and a password reset nobody asked for. Each clue is one query, and each query's answer tells you what to ask next. (Soko Safi and everyone in it are made up.)

## What you'll use

Four tables:

```
staff            (username, name, dept, joined_on, left_on, account_enabled)
logins           (id, username, ip, at, success)
exports          (id, username, table_name, row_count, at)
password_resets  (id, account, reset_by, at, ticket_id)
```

- `left_on` is someone's **last day**, and `NULL` if they still work there.
- `logins.username` is whatever was typed at the login box, so it isn't always a real account.
- `password_resets.ticket_id` is the help-desk ticket that asked for the reset. A reset is supposed to have one.

Everything comes from Phases 1 and 2: `WHERE`, `ORDER BY`, `LEFT JOIN`, a subquery with `IN`, `IS NULL`, `DISTINCT` and `UPDATE`. Two traps are waiting:

- **An inner join drops rows that have no partner.** Some accounts aren't people, so they aren't in `staff`. Clue 2 must keep them (Day 20).
- **A date isn't a time.** `at > left_on` compares a date and time with a date, and the date counts as midnight at the start of that day. So a login at 17:30 on someone's last day looks like it came after they left. Compare `DATE(at)` instead.

## Steps

```bash
tools/mysql.sh -e "CREATE DATABASE breach;"
tools/mysql.sh breach < phase-2-many-tables/extra-the-breach/setup.sql
```

Write each clue's query in `starter/`, run it, and read the answer before you write the next one:

1. `1-big_exports.sql`: who pulled the whole customer list out? Look at every big export of `customers`. Most come from the same account, every Monday at 02:00, which is the weekly marketing report. One doesn't.
2. `2-whose_account.sql`: whose accounts made those exports? One of them belongs to someone who had already left.
3. `3-ghost_logins.sql`: so how did anyone log in as them? Find every successful login by an account whose owner had left. Note the IP address.
4. `4-same_ip.sql`: an IP address is a place, such as a home Wi-Fi network. Who else, still working at Soko Safi, logged in from there?
5. `5-resets.sql`: a departed account's old password shouldn't work, so someone must have set a new one. Which resets had no ticket?
6. When you know, fill in `starter/answers.py`: the account used, the person really at the keyboard, and when the list left.
7. `pytest phase-2-many-tables/extra-the-breach`

The tests run each clue on the real logs, then add a few rows and run it again, so the query has to find the answer, not just name it. The final answers are stored as hashes, so reading the tests won't give them away.

Watch the red herrings. Someone abroad spent an early morning guessing passwords, and failed every time. Another departed employee tried their old password once. A third person reset a password without a ticket. Your job is to say which of these matter, and why.

## The kata: Close the Door

The breach worked because Joseph Otieno's account was still switched on nearly two weeks after he left. In `starter/kata.sql`, write one `UPDATE` that disables the account of **everyone** who has left, and nobody else's. The test adds someone who leaves at the end of the month before running it, so don't list usernames by hand.

## When you're stuck

- **Clue 2 has only one row**: you used `JOIN`. The marketing bot isn't in `staff`, so an inner join throws its exports away. Use `LEFT JOIN staff`.
- **Clue 3 shows a login from the day someone left**: that's the date-and-midnight trap. Use `DATE(l.at) > s.left_on`.
- **Clue 3 shows failed logins**: guessing a password isn't getting in. Keep only `success`.
- **Clue 4 lists the departed account itself**: leave out everyone whose `left_on` isn't `NULL`. A `NOT IN` subquery on `staff` does it.
- **Clue 5 returns nothing**: `ticket_id = NULL` is never true, not even for a `NULL`. Write `ticket_id IS NULL` (Day 11).
- **`WHEN` isn't accepted**: write the export's time as `"YYYY-MM-DD HH:MM"`.

## Why this matters at work

Every step here is a real control that failed:

- Accounts weren't switched off when people left.
- An IT person could reset a password without a ticket.
- Nobody looked at an export of the whole customer list in the middle of the night.

Under Kenya's Data Protection Act 2019, a leak like this has to be reported to the Data Commissioner. These five queries are the kind of thing an investigator runs first. In Day 94 you'll lock a database down so this is harder to do in the first place.
