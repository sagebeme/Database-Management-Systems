# Phase 4: worked examples

Nine exam-style problems with the working shown step by step. They sit outside the hundred days. Read them after Day 49 and before [Checkpoint 2](checkpoint-2-practice-test-2/README.md). Cover the working, try each one yourself, then compare.

Notation: `AB → C` means A and B together determine C. X⁺ is the closure of X: everything X determines.

---

## 1. Closure: does AC determine everything?

**R(A, B, C, D, E, F)** with A → B, C → D, AD → E, B → F. Find (AC)⁺ and A⁺.

Start with what you have and apply any dependency whose left side is already inside, until nothing changes:

| Step | Rule used | Closure so far |
|---|---|---|
| start | | A C |
| 1 | A → B | A B C |
| 2 | C → D | A B C D |
| 3 | AD → E (A and D are both in) | A B C D E |
| 4 | B → F | A B C D E F |

(AC)⁺ is all six attributes, so **AC is a superkey**. Neither A⁺ = {A, B, F} nor C⁺ = {C, D} is everything, so AC is also a **candidate key** (no smaller part of it works).

**The trap**: AD → E only fires once *both* A and D are in. People apply it as soon as A arrives.

---

## 2. Finding every candidate key

**R(A, B, C, D, E, F)** with AB → C, C → DE, E → F, F → B.

Sort the attributes first:

- **Never on a right side**: A. It can't be derived, so it's in **every** key.
- **Only on right sides**: D. It never helps derive anything, so it's in **no** key.
- **Both sides**: B, C, E, F. These are the ones to try.

A⁺ = {A}, not enough. Add one "both sides" attribute at a time:

- (AB)⁺ = AB → C → DE → F = all six. **Key.**
- (AC)⁺ = AC → DE → F → B = all six. **Key.**
- (AE)⁺ = AE → F → B, then AB → C → D = all six. **Key.**
- (AF)⁺ = AF → B, then AB → C → DE = all six. **Key.**

Every two-attribute set that works contains A, and every larger set containing A plus one of these isn't minimal. **Four candidate keys: AB, AC, AE, AF.** The prime attributes are A, B, C, E, F; D is the only non-prime one.

---

## 3. A minimal cover

**F = { AB → CD, A → C, C → D, B → D }.**

1. **One attribute on each right side**: AB → C, AB → D, A → C, C → D, B → D.
2. **Remove extra attributes on the left.** For AB → C: is C in A⁺? A⁺ = {A, C, D}. Yes, so B is extra and AB → C becomes A → C, which we already have. For AB → D: D is in A⁺ too, so it becomes A → D.
   Now: A → C, A → D, C → D, B → D.
3. **Remove redundant dependencies.** Take each one out and see whether the rest still imply it:
   - A → D: without it, A⁺ = {A, C, D}. Still implied, so **drop it**.
   - A → C: without it, A⁺ = {A}. Keep. C → D and B → D: likewise needed.

**Minimal cover: { A → C, C → D, B → D }**: three dependencies.

**Order matters**: do step 2 before step 3. Removing dependencies first can leave an extra attribute on a left side that you never notice.

---

## 4. Lossless or not: the quick test and the chase

**Two pieces.** R1 and R2 are a lossless split of R exactly when their common attributes determine all of R1 or all of R2.

R(A, B, C, D) with B → C, split into (A, B, D) and (B, C): the common attribute is B, and B⁺ ⊇ {B, C} = R2. **Lossless.** Split it into (A, B) and (C, D) instead and there's no common attribute at all: **lossy**.

**More than two pieces: the chase.** R(A, B, C, D, E) with A → C, B → C, C → D, DE → C, CE → A, split into (A, D), (A, B), (B, E), (C, D, E), (A, E).

Write one row per piece. Use `a` for the attributes it has and `b` (subscripted by row) for the rest:

| | A | B | C | D | E |
|---|---|---|---|---|---|
| AD | a | b1 | b1 | a | b1 |
| AB | a | a | b2 | b2 | b2 |
| BE | b3 | a | b3 | b3 | a |
| CDE | b4 | b4 | a | a | a |
| AE | a | b5 | b5 | b5 | a |

Apply each dependency: rows that agree on the left side must agree on the right. When one side has `a`, both become `a`. Otherwise both become the lower subscript.

- **A → C**: rows AD, AB and AE agree on A, so their C values all become b1.
- **B → C**: rows AB and BE agree on B, so BE's C becomes b1.
- **C → D**: rows AD, AB, BE and AE now share C = b1, and AD has D = `a`, so all four get D = `a`.
- **DE → C**: rows BE, CDE and AE agree on D and E (`a`, `a`), and CDE has C = `a`, so all three get C = `a`.
- **CE → A**: rows BE, CDE and AE agree on C and E, and AE has A = `a`, so all three get A = `a`.

Row BE is now `a a a a a`. **A row of all `a` means lossless.** If you get through every dependency without one, it's lossy.

---

## 5. Dependency preserving?

**R(A, B, C)** with A → B, B → C, C → A, split into (A, B) and (B, C).

C → A spans both pieces, so it looks lost. Don't give up yet: work out what holds *inside* each piece, using closures in the whole of F.

- In (A, B): A⁺ = ABC, so A → B; B⁺ = ABC, so B → A.
- In (B, C): B → C; C⁺ = ABC, so C → B.

Together: C → B and B → A, so **C → A still follows**. Every dependency of F is implied, so the split **preserves dependencies**. It's lossless too, because B (the common attribute) is a key.

**The lesson**: a dependency "crossing" two pieces is only lost if no chain inside the pieces rebuilds it.

---

## 6. The highest normal form

**R(A, B, C, D, E)** with A → B, A → C, BC → D, D → E.

1. **Keys**: A appears on no right side and A⁺ = everything, so **A is the only key**. Prime: A. Non-prime: B, C, D, E.
2. **2NF** (no non-prime attribute depends on *part* of a key): the key is a single attribute, so it has no proper parts. **In 2NF.**
3. **3NF** (for every X → Y, X is a superkey or Y is prime): BC → D has BC not a superkey and D non-prime. **Not in 3NF.**

**Highest: 2NF.** A one-attribute key always gives 2NF for free; that's a favourite exam shortcut.

---

## 7. 3NF synthesis

Same R(A, B, C, D, E), same dependencies.

1. **Minimal cover**: A → B, A → C, BC → D, D → E (already minimal).
2. **One relation per left side**, merging dependencies that share one: (A, B, C), (B, C, D), (D, E).
3. **Make sure some relation contains a key.** A is in (A, B, C), so nothing to add.
4. **Remove any relation contained in another.** None.

**Three relations: ABC, BCD, DE.** Synthesis is always lossless and dependency-preserving, and each piece is in 3NF.

---

## 8. BCNF can cost you a dependency

**Teaches(student, subject, teacher)**. A student takes each subject from one teacher (student, subject → teacher), and each teacher teaches one subject (teacher → subject).

- Keys: (student, subject) and (student, teacher). Every attribute is prime, so the table is in **3NF**.
- teacher → subject has teacher not a superkey, so it's **not in BCNF**.

Decompose on the violating teacher → subject: (teacher, subject), and the rest, (student, teacher). It's lossless, because the common attribute, teacher, determines (teacher, subject).

But **student, subject → teacher is gone**: no piece has all three, and nothing inside the pieces rebuilds it. The database can no longer stop a student having two teachers for one subject.

**The rule exams test**: a lossless BCNF decomposition always exists, but sometimes it can't preserve dependencies. 3NF can always do both. That's why 3NF is the usual practical target.

---

## 9. Multivalued dependencies and 4NF

**Teaching(teacher, subject, book)**: each teacher teaches several subjects and uses several books, and the books don't depend on the subject.

| teacher | subject | book |
|---|---|---|
| Wanjiru | Maths | KLB Bk 3 |
| Wanjiru | Maths | Spotlight |
| Wanjiru | Physics | KLB Bk 3 |
| Wanjiru | Physics | Spotlight |

There are no functional dependencies apart from the trivial ones, so the only key is all three columns and the table is in **BCNF**. Yet adding one book for Wanjiru means adding a row for *every* subject she teaches: an anomaly.

The cause is two **multivalued dependencies**, teacher →→ subject and teacher →→ book. They come as a pair: if X →→ Y holds, so does X →→ (R − X − Y). Neither has a superkey on the left, so the table isn't in **4NF**. Split it into (teacher, subject) and (teacher, book), each with no non-trivial MVD.

**Facts to remember**: every FD is also an MVD; 4NF implies BCNF, but not the other way round.
