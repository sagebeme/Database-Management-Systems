# Day 40: Capstone: Design a Hospital

## The brief

Dr Wekesa, the medical superintendent of a county referral hospital, is replacing the outpatient clinic's paper registers. You're designing the database. Here is her brief, word for word as she gave it:

> "We have **departments**: Outpatient, Paediatrics, Maternity, Dental, Eye. Department names are unique. Every **doctor** works in exactly one department, and each has a medical licence number, which no two doctors share. A department may have no doctors yet: Eye is waiting for one.
>
> We register **patients** with their name, date of birth, phone and national ID. Children don't have national IDs, but no two adults share one. Phones are Kenyan mobile numbers in the 254 format. A patient can name several **next of kin**, each with a relationship and a phone number; we know them only through the patient, and each patient names a given person once. If a patient's record is ever removed, their next of kin go with it.
>
> Every **visit** is one patient seeing one doctor at a date and time. The diagnosis is sometimes filled in later. Medical records are kept for years: **you must never be able to delete a patient or a doctor who has visits on record.**
>
> At a visit, the doctor may prescribe **drugs**. Each drug has a unique name and a unit price in shillings and cents, never negative. A **prescription** says how many units of one drug for one visit, at least one, and a visit lists each drug once."

There's no walkthrough. This is Phase 3's design work from end to end: the diagram, the tables, the constraints, and the questions the hospital will ask.

## What you'll use

Days 15–38: keys and constraints (16, 17, 30, 31), ER diagrams and their mapping (32–34), joins and anti-joins (19–22), aggregates (23), views (26) and division (37).

**The contract.** The hospital's app developers are building against these table and column names, so use exactly these. Everything else (types, keys, `NULL` or not, `UNIQUE`, `CHECK`, foreign keys and their `ON DELETE`) is yours to decide from the brief:

| Table | Columns |
|---|---|
| `departments` | `id`, `name` |
| `doctors` | `id`, `name`, `licence_no`, `department_id` |
| `patients` | `id`, `name`, `national_id`, `born_on`, `phone` |
| `next_of_kin` | `patient_id`, `name`, `relationship`, `phone` |
| `visits` | `id`, `patient_id`, `doctor_id`, `visited_at`, `diagnosis` |
| `drugs` | `id`, `name`, `unit_price` |
| `prescriptions` | `visit_id`, `drug_id`, `quantity` |

## Steps

1. `starter/hospital.mmd`: the ER diagram, with all seven entities, their keys, and every relationship with the right symbols at both ends. Which entity is weak? Which pair is really many-to-many, with `PRESCRIPTION` in the middle?
2. `starter/schema.sql`: the seven tables. Then test them against the data:

   ```bash
   tools/mysql.sh -e "DROP DATABASE IF EXISTS hospital; CREATE DATABASE hospital;"
   tools/mysql.sh hospital < phase-3-design/day-040-capstone-design-a-hospital/starter/schema.sql
   tools/mysql.sh hospital < phase-3-design/day-040-capstone-design-a-hospital/data.sql
   ```

   The tests try to break every rule in the brief. Try a few yourself first.
3. The queries. Each file is one `SELECT`; column names and orders are part of the answer:

| File | The question | Columns |
|---|---|---|
| `0-doctors_per_department.sql` | Every department and its number of doctors, zero included. Most first, ties alphabetical | `department`, `doctors` |
| `1-busiest_doctors.sql` | Every doctor and the visits they've seen, zero included. Most first, ties alphabetical | `doctor`, `visits` |
| `2-patient_history.sql` | Wanjiru Kamau's visits (by name), oldest first | `visited_at`, `doctor`, `department`, `diagnosis` |
| `3-visit_bills.sql` | Every visit's drug bill: quantity × unit price, summed; `0.00` with no prescriptions. In visit order | `visit_id`, `patient`, `total` |
| `4-never_visited.sql` | Registered patients with no visits. Alphabetical | `name` |
| `5-seen_by_every_outpatient_doctor.sql` | Patients seen by every doctor in Outpatient. Alphabetical | `name` |

4. `pytest phase-3-design/day-040-capstone-design-a-hospital`

The query tests run on the reference schema, and again after a shake-up (a new Outpatient doctor, Njeri's first visit, a newly registered patient, more prescriptions).

## The kata: The Pharmacy Board

In `starter/kata.sql`, create the view `drug_usage`: every drug, how many prescriptions name it, and the total units prescribed, with zeros for drugs nobody has prescribed. Columns `drug`, `prescriptions`, `units`.

## When you're stuck

- **The contract test fails**: it lists the columns it found. A typo in one column name is enough; so is an extra table.
- **"a patient with visits can't be deleted" fails**: the default (`RESTRICT`) already refuses. You probably wrote `ON DELETE CASCADE` on `visits`. Cascade belongs on `next_of_kin` only.
- **Two children can't both be registered**: `national_id` must allow `NULL`, and `UNIQUE` allows many `NULL`s (Day 16).
- **Prices come back as `120`**: use `DECIMAL(8, 2)`, not `INT` or `FLOAT`. Money is never a float.
- **Visit 9's bill is `NULL`**: `SUM` over no rows is `NULL`. Wrap it in `COALESCE(..., 0.00)`.
- **The division is right on the data but wrong after the shake-up**: with Dr Odera added, only Wanjiru has seen all three Outpatient doctors. Use the double `NOT EXISTS` from Day 37, not a count that compares with 2.
- **Done?** That's Phase 3. Phase 4 asks the question you've been answering by instinct all along: how do you *know* a design is good? The answer is functional dependencies and normal forms.
