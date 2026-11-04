"""Day 32: attributes and the symbols of a Chen ER diagram.

For a customer's attributes, answer with one of:
    "simple", "composite", "multivalued", "derived"

For the Chen symbols, answer with one of:
    "entity", "weak entity", "relationship", "identifying relationship", "attribute",
    "key attribute", "multivalued attribute", "derived attribute", "total participation"
"""

# A customer has ...
EMAIL = "simple"                  # one email address
FULL_NAME = "composite"              # first name, middle name and surname
PHONE_NUMBERS = "multivalued"          # any number of phone numbers
AGE = "derived"                    # worked out from date_of_birth
DATE_OF_BIRTH = "simple"          # a single date
HOME_ADDRESS = "composite"           # county, town, estate and house number

# In a Chen diagram, what does each shape mean?
RECTANGLE = "entity"
DOUBLE_RECTANGLE = "weak entity"
DIAMOND = "relationship"
DOUBLE_DIAMOND = "identifying relationship"
ELLIPSE = "attribute"
UNDERLINED_ELLIPSE = "key attribute"
DOUBLE_ELLIPSE = "multivalued attribute"
DASHED_ELLIPSE = "derived attribute"
DOUBLE_LINE = "total participation"

# How do you store each kind in tables? Answer with one of:
#   "one column", "one column per part", "a table of its own", "not stored, calculated"
STORE_COMPOSITE = "one column per part"
STORE_MULTIVALUED = "a table of its own"
STORE_DERIVED = "not stored, calculated"
