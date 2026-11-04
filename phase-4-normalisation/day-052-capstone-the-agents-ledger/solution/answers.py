"""Day 52: the design, before the SQL. Replace each None.

ledger_raw's attributes: code, date_time, till, agent_name, location, phone, customer_name, txn_type, amount,
commission. Each code is one transaction. A till always belongs to the same agent (name and location); a phone
number to the same customer.
"""

# The functional dependencies, in Day 41's notation, e.g. "a b -> c; c -> d". Names with spaces between them.
RAW_FDS = "code -> date_time till phone txn_type amount commission; till -> agent_name location; phone -> customer_name"

# The candidate key (a set of names) and the highest normal form ledger_raw is in ("1NF", "2NF", "3NF", "BCNF").
KEY = {"code"}
HIGHEST_NF = "2NF"

# The 3NF synthesis of ledger_raw (Day 49): a set of frozensets of names.
PARTS = {frozenset({"code", "date_time", "till", "phone", "txn_type", "amount", "commission"}),
         frozenset({"till", "agent_name", "location"}), frozenset({"phone", "customer_name"})}

# True or False
COMMISSION_SHOULD_BE_WORKED_OUT_FROM_TODAYS_RATES_INSTEAD_OF_STORED = False
THE_NEW_TABLES_ARE_IN_BCNF = True
