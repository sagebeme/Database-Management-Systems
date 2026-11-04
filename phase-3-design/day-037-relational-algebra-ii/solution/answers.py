"""Day 37: joins and division. Replace each None.

R(A, B) has 6 tuples and S(B, C) has 4. Every B value is unique within S.
"""

MOST_TUPLES_IN_R_NATURAL_JOIN_S = 6     # each R tuple can match at most one S tuple
MOST_TUPLES_IN_R_LEFT_JOIN_S = 6
FEWEST_TUPLES_IN_R_LEFT_JOIN_S = 6
DEGREE_OF_R_NATURAL_JOIN_S = 3

# One of "select", "project", "rename", "union", "difference", "product"
A_THETA_JOIN_IS_A_PRODUCT_FOLLOWED_BY = "select"

# Which operator answers "which students took EVERY core unit"? One of "join", "union", "division", "semi-join"
EVERY_QUESTIONS_NEED = "division"

# True or False: if S is empty, R ÷ S returns every A value in R.
DIVIDING_BY_AN_EMPTY_RELATION_RETURNS_EVERYTHING = True
