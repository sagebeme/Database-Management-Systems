"""Day 45: covers on paper. Replace each None.

F = { A -> BC,  B -> C,  A -> B,  AB -> C }
"""

FDS_IN_THE_MINIMAL_COVER_OF_F = 2         # how many, after splitting right sides
FDS_IN_THE_CANONICAL_COVER_OF_F = 2
EXTRANEOUS_ATTRIBUTE_IN_AB_TO_C = "B"        # one letter

# True or False
A_MINIMAL_COVER_IS_ALWAYS_UNIQUE = False
A_MINIMAL_COVER_IS_EQUIVALENT_TO_F = True
REMOVE_REDUNDANT_FDS_BEFORE_EXTRANEOUS_ATTRIBUTES = False   # is that the safe order?
