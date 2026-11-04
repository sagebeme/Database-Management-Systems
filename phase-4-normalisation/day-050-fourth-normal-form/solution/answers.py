"""Day 50: MVDs and 4NF. Replace each None.

A school keeps R(course, teacher, book): every teacher of a course uses every book of that course.
"""

# The two parts R splits into for 4NF, as a set of frozensets of names.
COURSE_PARTS = {frozenset({"course", "teacher"}), frozenset({"course", "book"})}

# Databases has 3 books. A new teacher joins it. How many rows does R need for that?
ROWS_IN_R_FOR_A_NEW_TEACHER = 3
# And how many rows in the split tables?
ROWS_SPLIT_FOR_A_NEW_TEACHER = 1

# Back at the tuition centre: how many rows would tutor_offers need for Achieng's Chemistry (step 2)?
ROWS_OLD_TABLE_NEEDS_FOR_ACHIENGS_CHEMISTRY = 3

# True or False
EVERY_FD_IS_AN_MVD = True
EVERY_MVD_IS_AN_FD = False
A_RELATION_IN_4NF_IS_IN_BCNF = True
A_BCNF_RELATION_IS_ALWAYS_IN_4NF = False
IF_X_MVD_Y_THEN_X_MVD_THE_REST = True
