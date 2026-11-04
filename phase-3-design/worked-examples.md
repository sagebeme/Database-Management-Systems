# Phase 3: worked examples

Eight exam-style problems with the working shown step by step. They sit outside the hundred days. Read them after Day 38 and before [Practice Test 1](day-039-practice-test-1/README.md). Cover the working, try each one yourself, then compare.

---

## 1. Counting superkeys

**R(A, B, C, D, E)** has exactly two candidate keys: {A} and {B, C}. How many superkeys does it have?

A superkey is any set that contains a candidate key. Count the sets containing each key, then remove the double count (inclusion and exclusion):

- Containing A: the other 4 attributes are each in or out, so 2⁴ = **16**.
- Containing B and C: the other 3 are free, so 2³ = **8**.
- Containing A, B and C (counted in both): the other 2 are free, so 2² = **4**.

16 + 8 − 4 = **20 superkeys**.

**The trap**: adding 16 + 8 counts sets like {A, B, C} twice.

---

## 2. The fewest tables for an ER diagram

A school's diagram has:

- **Student**, with a multivalued attribute *phone*;
- **Department**, 1:N to Student, and every student is in a department (total participation on the Student side);
- **Course**, M:N to Student through *Enrols*, which has its own attribute *grade*;
- **Room**, 1:1 with Course, where some rooms have no course.

Go through it piece by piece:

| Piece | Rule | Tables |
|---|---|---|
| Student, Department, Course, Room | each strong entity gets a table | 4 |
| phone (multivalued) | always its own table: (student_id, phone) | +1 |
| Department 1:N Student | put department_id in Student (the "many" side); no table | 0 |
| Enrols, M:N with grade | always its own table: (student_id, course_id, grade) | +1 |
| Course 1:1 Room | put room_id in Course; no table | 0 |

**Six tables.** The rules that decide every question like this:

- An **M:N** relationship always needs its own table.
- A **1:N** relationship never does: the foreign key goes on the N side.
- A **1:1** relationship never does either; it can even merge the two entities into one table, but only if both sides participate totally.
- A **multivalued attribute** always needs its own table.

---

## 3. A weak entity's key

**Dependant**(name, birth_date) belongs to **Employee**(emp_no, ...) through an identifying relationship. Two employees can both have a dependant called "Imani".

- The dependant's own *partial key* is `name`. It's unique only within one employee.
- Its table's primary key is the **owner's key plus the partial key**: (emp_no, name).
- emp_no is also a foreign key to Employee, normally `ON DELETE CASCADE`: a dependant can't exist without their employee.

---

## 4. How big can a join be?

R(A, B) has 10 rows and S(B, C) has 20, with no `NULL`s. How many rows can R ⋈ S have?

- **Fewest**: 0, if no B value appears in both.
- **Most**: 10 × 20 = 200, if every row has the same B.

Now add facts one at a time:

- **B is S's primary key**: each R row matches at most one S row, so at most **10**.
- **And R.B is a foreign key to S, `NOT NULL`**: each R row matches *exactly* one, so exactly **10**.

Keys bring the maximum down; a foreign key plus `NOT NULL` fixes the exact count.

---

## 5. Division, step by step

Enrol(student, course) and Required(course):

| student | course |
|---|---|
| Amina | DB |
| Amina | OS |
| Brian | DB |
| Chege | DB |
| Chege | OS |
| Chege | AI |
| Dama | OS |

Required = {DB, OS}. Who has taken **every** required course? That's Enrol ÷ Required, built from the basic operators:

```
Enrol ÷ Required = π_student(Enrol) − π_student( (π_student(Enrol) × Required) − Enrol )
```

1. π_student(Enrol) = {Amina, Brian, Chege, Dama}.
2. × Required gives the 8 pairs each student *should* have.
3. − Enrol leaves the pairs that are **missing**: (Brian, OS) and (Dama, DB).
4. π_student of those: the students missing something, {Brian, Dama}.
5. All students minus those: **{Amina, Chege}**.

Chege's extra AI course doesn't matter: division asks "at least all of these".

---

## 6. Projection doesn't distribute over difference

Is π_A(R − S) the same as π_A(R) − π_A(S)? Try a tiny example, R = {(1, x)} and S = {(1, y)} on (A, B):

- R − S = {(1, x)}, so π_A(R − S) = **{1}**.
- π_A(R) = {1} and π_A(S) = {1}, so π_A(R) − π_A(S) = **∅**.

They differ. **Selection** does distribute over union, intersection and difference; **projection** distributes over union only. One counterexample of two rows settles any question like this.

---

## 7. Outer join row counts

R(A) = {1, 2, 3} and S(A) = {2, 3, 3, 4}. How many rows does each join return?

- **Inner join** on A: 2 matches one S row and 3 matches two, so **3 rows**.
- **Left outer**: those 3, plus 1 (no match, padded with `NULL`), so **4**.
- **Right outer**: those 3, plus 4 (no match), so **4**.
- **Full outer**: those 3, plus 1 and 4, so **5**.

Count the matched pairs first, then add one row for each unmatched row on the side(s) you keep.

---

## 8. Tuple calculus: "every" and safety

**Students who have taken every required course**, in tuple relational calculus:

```
{ t | ∃e ∈ Enrol (t.student = e.student) ∧
      ∀r ∈ Required ( ∃f ∈ Enrol (f.student = t.student ∧ f.course = r.course) ) }
```

Read it aloud: t is a student who appears in Enrol, and for every required course r, there's an Enrol row pairing t with r. That's division again (example 5).

**Safety**: { t | ¬(t ∈ Enrol) } asks for every tuple in the universe that isn't in Enrol: infinitely many. It's **unsafe**. A safe query only returns values that appear in the database or in the query itself. The first line above, tying t to an Enrol row, is what keeps the "every" query safe.
