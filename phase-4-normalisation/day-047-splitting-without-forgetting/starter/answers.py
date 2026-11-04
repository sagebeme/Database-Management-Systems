"""Day 47: dependency preservation. Replace each None with True or False."""

# R(A, B, C, D), F = { A -> B, B -> C, C -> D, D -> A }, split into AB, BC, CD.
D_TO_A_IS_PRESERVED = None
THE_SPLIT_IS_DEPENDENCY_PRESERVING = None

# R(A, B, C), F = { AB -> C, C -> A }, split into AC and BC.
AB_TO_C_IS_PRESERVED = None
THIS_SPLIT_IS_LOSSLESS = None

# R(A, B, C, D), F = { A -> B, C -> D }, split into AB and CD.
THAT_SPLIT_IS_DEPENDENCY_PRESERVING = None
THAT_SPLIT_IS_LOSSLESS = None

# In general
EVERY_RELATION_HAS_A_LOSSLESS_DEPENDENCY_PRESERVING_3NF_SPLIT = None
EVERY_RELATION_HAS_A_LOSSLESS_DEPENDENCY_PRESERVING_BCNF_SPLIT = None
