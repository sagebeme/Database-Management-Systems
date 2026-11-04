"""Day 46: lossless joins. Replace each None.

R(A, B, C, D) with F = { A -> B, C -> D }
"""

# True or False: is each split lossless?
AB_AND_CD = False
AB_AND_ACD = True
ABC_AND_CD = True
AC_AND_BD = False

# True or False
A_LOSSY_JOIN_LOSES_ROWS = False            # (careful: what does it really do?)
A_LOSSY_JOIN_ADDS_ROWS_THAT_WERENT_THERE = True
