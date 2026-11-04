"""Day 35: the relational model's words. Replace each None."""

# Which relational term matches each everyday word? One of:
#   "relation", "tuple", "attribute", "domain", "degree", "cardinality", "schema", "instance"
TABLE = "relation"
ROW = "tuple"
COLUMN = "attribute"
ALLOWED_VALUES_OF_A_COLUMN = "domain"
NUMBER_OF_COLUMNS = "degree"
NUMBER_OF_ROWS = "cardinality"
THE_TABLE_DEFINITION = "schema"          # name and attributes: towns(name, county)
THE_ROWS_RIGHT_NOW = "instance"            # the data at one moment

# True or False
ORDER_OF_TUPLES_MATTERS = False
A_RELATION_CAN_HOLD_THE_SAME_TUPLE_TWICE = False
AN_SQL_TABLE_CAN_HOLD_THE_SAME_ROW_TWICE = True   # with no key
SELECT_WITHOUT_DISTINCT_CAN_RETURN_DUPLICATES = True
