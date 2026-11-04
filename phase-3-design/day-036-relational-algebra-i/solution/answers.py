"""Day 36: sizes and facts about the operators. Replace each None.

R and S are union-compatible, with |R| = 10 and |S| = 6. T has 4 tuples and no attribute
names in common with R. R has degree 3, T has degree 2.
"""

MOST_TUPLES_IN_R_UNION_S = 16
FEWEST_TUPLES_IN_R_UNION_S = 10
MOST_TUPLES_IN_R_MINUS_S = 10
FEWEST_TUPLES_IN_R_MINUS_S = 4
TUPLES_IN_R_TIMES_T = 40
DEGREE_OF_R_TIMES_T = 5
MOST_TUPLES_IN_A_SELECTION_OF_R = 10
FEWEST_TUPLES_IN_A_PROJECTION_OF_R = 1       # R isn't empty

# True or False
INTERSECTION_IS_ONE_OF_THE_BASIC_SIX = False
SELECT_THEN_SELECT_EQUALS_ONE_SELECT_WITH_AND = True   # sigma_p(sigma_q(R)) = sigma_(p and q)(R)
UNION_IS_COMMUTATIVE = True                           # R ∪ S = S ∪ R
DIFFERENCE_IS_COMMUTATIVE = False                      # R − S = S − R
