"""Day 38: relational calculus. Replace each None."""

# Which of these is UNSAFE (its answer could be infinite)? "A", "B" or "C"
#   A: { t | t ∈ SHOWS ∧ t.year > 2020 }
#   B: { t | ¬(t ∈ SHOWS) }
#   C: { t | ∃ s ∈ SHOWS (t.title = s.title ∧ t.year = s.year) ∧ t ∈ RATED }
THE_UNSAFE_ONE = "B"

# What do the variables range over? "tuples" or "domain values"
TRC_VARIABLES_RANGE_OVER = "tuples"
DRC_VARIABLES_RANGE_OVER = "domain values"

# True or False
RELATIONAL_ALGEBRA_IS_PROCEDURAL = True      # it says HOW: an order of operations
RELATIONAL_CALCULUS_IS_PROCEDURAL = False     # it says WHAT the answer is
SAFE_CALCULUS_AND_ALGEBRA_CAN_EXPRESS_THE_SAME_QUERIES = True

# ∀ x (P) can be rewritten as ¬∃ x (¬P). How do you write it in SQL? "NOT EXISTS" or "IN" or "JOIN"
SQL_FOR_ALL = "NOT EXISTS"
