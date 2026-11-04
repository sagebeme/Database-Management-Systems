"""Day 47: dependency preservation. Replace each None with True or False."""

# R(A, B, C, D), F = { A -> B, B -> C, C -> D, D -> A }, split into AB, BC, CD.
D_TO_A_IS_PRESERVED = True
THE_SPLIT_IS_DEPENDENCY_PRESERVING = True

# R(A, B, C), F = { AB -> C, C -> A }, split into AC and BC.
AB_TO_C_IS_PRESERVED = False
THIS_SPLIT_IS_LOSSLESS = True

# R(A, B, C, D), F = { A -> B, C -> D }, split into AB and CD.
THAT_SPLIT_IS_DEPENDENCY_PRESERVING = True
THAT_SPLIT_IS_LOSSLESS = False

# In general
EVERY_RELATION_HAS_A_LOSSLESS_DEPENDENCY_PRESERVING_3NF_SPLIT = True
EVERY_RELATION_HAS_A_LOSSLESS_DEPENDENCY_PRESERVING_BCNF_SPLIT = False
