"""Day 44: Armstrong's axioms. Replace each None.

Name the rule used in each step. One of:
    "reflexivity", "augmentation", "transitivity", "union", "decomposition", "pseudotransitivity"
"""

AB_TO_A = "reflexivity"                          # AB -> A, from nothing at all
A_TO_B_GIVES_AC_TO_BC = "augmentation"            # from A -> B
A_TO_B_AND_B_TO_C_GIVES_A_TO_C = "transitivity"
A_TO_B_AND_A_TO_C_GIVES_A_TO_BC = "union"
A_TO_BC_GIVES_A_TO_B = "decomposition"
A_TO_B_AND_CB_TO_D_GIVES_AC_TO_D = "pseudotransitivity"

# True or False
THE_AXIOMS_ARE_SOUND = True             # they never derive an FD that doesn't really follow
THE_AXIOMS_ARE_COMPLETE = True          # they derive every FD that does follow
UNION_IS_ONE_OF_THE_THREE_AXIOMS = False # (it's derived from them)
AB_TO_C_GIVES_A_TO_C = False             # can you split a LEFT side?
