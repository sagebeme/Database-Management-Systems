"""Day 91: reading query plans. Replace each None."""

# The join node in your 1-explain.sql plan: "Nested Loop", "Hash Join" or "Merge Join".
COUNTY_REPORT_JOIN = None
# With idx_orders_customer in place, the join node in the plan for
#   SELECT c.name, o.total FROM customers AS c JOIN orders AS o ON o.customer_id = c.id WHERE c.id = 42;
ONE_CUSTOMER_JOIN = None
# ...and for
#   SELECT c.name, o.total FROM customers AS c JOIN orders AS o ON o.customer_id = c.id ORDER BY c.id;
SORTED_JOIN = None
# How many rows the Hash node in your county report plan says it held (its "actual rows").
ROWS_IN_THE_HASH = None

# True or False
A_HASH_JOIN_NEEDS_AN_EQUALITY_CONDITION = None
A_NESTED_LOOP_JOIN_CAN_JOIN_ON_ANY_CONDITION = None
EXPLAIN_WITHOUT_ANALYZE_RUNS_THE_QUERY = None
