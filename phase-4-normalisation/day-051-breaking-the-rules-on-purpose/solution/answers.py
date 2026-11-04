"""Day 51: denormalisation. Replace each None.

orders (id, shop_id, shop_name, placed_on, total) and shops (id, name, phone)
"""

# Which column of orders is a copy of something stored elsewhere? A set of names.
REDUNDANT_COLUMNS = {"shop_name"}

# The shop is renamed. With that design, how many tables need an UPDATE? (1 or 2)
TABLES_TO_UPDATE_ON_RENAME = 2

# True or False
A_SUMMARY_TABLE_CAN_GO_STALE = True
DENORMALISING_MAKES_WRITES_CHEAPER = False
A_MYSQL_VIEW_STORES_ITS_ROWS = False
NORMALISE_FIRST_THEN_DENORMALISE_WHAT_A_MEASUREMENT_SAYS_IS_SLOW = True
