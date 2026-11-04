"""Day 48: 1NF and 2NF. Replace each None."""

# R(student, course, name, fee, grade) with
#   student -> name,  course -> fee,  student course -> grade
CANDIDATE_KEY = {"student", "course"}                  # a set of attribute names
NON_PRIME_ATTRIBUTES = {"name", "fee", "grade"}           # a set of attribute names
IS_R_IN_2NF = False                    # True or False

# True or False
A_TABLE_WITH_A_COMMA_SEPARATED_LIST_COLUMN_IS_IN_1NF = False
A_RELATION_WHOSE_KEYS_ARE_ALL_SINGLE_ATTRIBUTES_IS_IN_2NF = True
TWO_NF_RESTRICTS_PRIME_ATTRIBUTES_TOO = False
A_PARTIAL_DEPENDENCY_NEEDS_A_COMPOSITE_KEY = True
