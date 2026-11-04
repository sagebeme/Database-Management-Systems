"""Day 49: 3NF and BCNF. Replace each None.

For each relation, the highest normal form it's in: "1NF", "2NF", "3NF" or "BCNF".
"""

R1 = "2NF"    # R(A, B, C),        F = { A -> B, B -> C }
R2 = "3NF"    # R(A, B, C),        F = { AB -> C, C -> B }
R3 = "1NF"    # R(A, B, C, D),     F = { AB -> CD, A -> C }
R4 = "BCNF"    # R(A, B),           F = { A -> B }
R5 = "3NF"    # R(A, B, C, D, E),  F = { A -> B, BC -> E, ED -> A }

# True or False
EVERY_BCNF_RELATION_IS_IN_3NF = True
EVERY_TWO_ATTRIBUTE_RELATION_IS_IN_BCNF = True
BCNF_DECOMPOSITION_ALWAYS_PRESERVES_DEPENDENCIES = False
THREE_NF_SYNTHESIS_ALWAYS_PRESERVES_DEPENDENCIES = True
