"""Day 30: questions about keys. Replace each None with your answer."""

# R(A, B, C, D) has exactly two candidate keys: {A} and {B, C}.
SUPERKEYS_OF_R = 10          # how many superkeys does R have? (an int)
PRIME_ATTRIBUTES_OF_R = {"A", "B", "C"}   # the attributes that belong to some candidate key (a set of strings)

# True or False
EVERY_CANDIDATE_KEY_IS_A_SUPERKEY = True
EVERY_SUPERKEY_IS_A_CANDIDATE_KEY = False
A_PRIMARY_KEY_COLUMN_CAN_BE_NULL = False
A_FOREIGN_KEY_COLUMN_CAN_BE_NULL = True
A_TABLE_CAN_HAVE_TWO_PRIMARY_KEYS = False
A_FOREIGN_KEY_MUST_POINT_AT_A_KEY = True
SAMPLE_DATA_CAN_PROVE_A_COLUMN_IS_A_KEY = False
