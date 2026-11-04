# Day 33: One, Many, Many-to-Many

## The brief

The IEBC's data team is redrawing its registration database, and every line on their ER diagram starts an argument. Does a person hold *one* national ID, or *at most* one? Must every county have a constituency, or only may it? Is a doctor always assigned a consulting room? Each answer changes the symbols at the ends of a line, and those symbols decide the tables.

Today is about the two numbers at each end of a relationship, and what they become in SQL.

## What you'll use

**Cardinality ratio** is the *maximum* at each end:

| Ratio | Example | In tables |
|---|---|---|
| 1:1 | a person holds one national ID | a foreign key on either side, made `UNIQUE` |
| 1:N | a county contains many constituencies | a foreign key on the **many** side |
| M:N | students register for many units, units have many students | a junction table (Day 21) |

**Participation** is the *minimum*: is every row of this entity *required* to take part?

- **Total** (minimum 1): every constituency is in some county. Chen draws a double line; Mermaid uses `|` (`||` or `|{`).
- **Partial** (minimum 0): a person may not have an ID yet. Mermaid uses `o` (`o|` or `o{`).

Total participation on the many side is easy to enforce: make the foreign key `NOT NULL`. Total participation on the **one** side ("every county has at least one constituency") **can't** be enforced by keys at all, because a new county has no constituencies yet when you insert it. It's a rule the application, or a trigger, has to keep.

**The fewest tables** for an ER diagram, a classic exam question:

1. Every entity set (strong or weak) gets a table.
2. Every multivalued attribute gets a table.
3. An **M:N** relationship gets a table.
4. A **1:N** relationship needs no table: put the foreign key on the N side.
5. A **1:1** relationship needs no table. If participation is **total on both sides**, the two entities can even share one table, so subtract one.

```
E1 ──M:N── E2                 E1, E2, E1_E2           3 tables
E1 ──1:N── E2                 E1, E2 (E2 has e1_id)   2 tables
E1 ══1:1══ E2 (both total)    E1_E2 together          1 table
```

## Steps

```bash
tools/mysql.sh -e "CREATE DATABASE IF NOT EXISTS design;"
tools/mysql.sh design < phase-3-design/day-033-one-many-many-to-many/setup.sql
```

1. `starter/relationships.mmd`: draw these five, with exactly the right symbols:
   - `COUNTY` contains `CONSTITUENCY`: each constituency is in exactly one county; each county has at least one constituency.
   - `PERSON` holds `NATIONAL_ID`: each person holds zero or one; each ID belongs to exactly one person.
   - `STUDENT` registers for `UNIT`: any number either way, including none.
   - `MATATU` belongs to `SACCO`: each matatu belongs to exactly one sacco; a sacco can have none yet, or many.
   - `DOCTOR` is assigned `CONSULTING_ROOM`: each doctor has at most one room, each room at most one doctor.
2. `starter/mapping.py`, `min_tables`: the rules above, as code.
3. `starter/answers.py`: the exam questions.
4. `starter/0-national_ids.sql`: `national_ids`: `id_no` (`CHAR(8)`, primary key) and `person_id`. A person holds at most one ID; every ID belongs to exactly one person.
5. `starter/1-constituencies.sql`: `constituencies`: `id` (auto-numbered primary key), `name` (`VARCHAR(60)`, required) and `county_code`: every constituency is in exactly one real county.
6. `pytest phase-3-design/day-033-one-many-many-to-many`

## The kata: Read the Diagram

In `starter/mapping.py`, write `describe(path)`: it reads a Mermaid file with `coursekit.er` and turns each relationship into two plain-English sentences, one from each side. Run it on your `relationships.mmd` and read the result aloud. If a sentence sounds wrong, the diagram is wrong.

## When you're stuck

- **Which end does a symbol describe?** The symbol *next to* an entity says how many of **that** entity go with one of the other. In `PERSON ||--o| NATIONAL_ID`, the `o|` next to `NATIONAL_ID` says a person has zero or one ID.
- **`STUDENT }o--o{ UNIT`**: many-to-many has a "many" symbol at both ends.
- **A person can get two IDs**: the foreign key needs `UNIQUE` as well. That's what makes it 1:1 instead of 1:N.
- **`TABLES_Q5`**: three entities, plus one for the M:N relationship. The 1:1 is total on only *one* side, so nothing merges.
- **`from coursekit import er` fails** when you run `mapping.py` yourself: run it through `pytest`, or start Python from the course folder with `PYTHONPATH=tools`.
