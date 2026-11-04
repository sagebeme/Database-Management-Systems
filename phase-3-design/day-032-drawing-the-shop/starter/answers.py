"""Day 32: attributes and the symbols of a Chen ER diagram.

For a customer's attributes, answer with one of:
    "simple", "composite", "multivalued", "derived"

For the Chen symbols, answer with one of:
    "entity", "weak entity", "relationship", "identifying relationship", "attribute",
    "key attribute", "multivalued attribute", "derived attribute", "total participation"
"""

# A customer has ...
EMAIL = None                  # one email address
FULL_NAME = None              # first name, middle name and surname
PHONE_NUMBERS = None          # any number of phone numbers
AGE = None                    # worked out from date_of_birth
DATE_OF_BIRTH = None          # a single date
HOME_ADDRESS = None           # county, town, estate and house number

# In a Chen diagram, what does each shape mean?
RECTANGLE = None
DOUBLE_RECTANGLE = None
DIAMOND = None
DOUBLE_DIAMOND = None
ELLIPSE = None
UNDERLINED_ELLIPSE = None
DOUBLE_ELLIPSE = None
DASHED_ELLIPSE = None
DOUBLE_LINE = None

# How do you store each kind in tables? Answer with one of:
#   "one column", "one column per part", "a table of its own", "not stored, calculated"
STORE_COMPOSITE = None
STORE_MULTIVALUED = None
STORE_DERIVED = None
