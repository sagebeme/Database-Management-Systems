"""Day 69: conflict serializability. Replace each None."""

# For S = r1(A) r2(B) w1(B) w2(A) r3(A): the precedence graph's edges, as a set of (i, j) pairs.
S_EDGES = {(1, 2), (2, 1), (2, 3)}
# Is S conflict serializable? (True or False)
S_IS_CONFLICT_SERIALIZABLE = False

# T1 = r1(A) w1(A) and T2 = r2(A) w2(A): how many interleavings are there in all, and how many are conflict
# serializable?
INTERLEAVINGS = 6
SERIALIZABLE_INTERLEAVINGS = 2

# True or False
TWO_READS_OF_THE_SAME_ITEM_CONFLICT = False
A_SERIAL_SCHEDULE_IS_ALWAYS_CONFLICT_SERIALIZABLE = True
