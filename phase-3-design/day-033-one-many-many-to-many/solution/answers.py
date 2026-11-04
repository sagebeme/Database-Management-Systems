"""Day 33: GATE-style questions about turning ER diagrams into tables. Replace each None."""

# Fewest tables (an int) for each diagram. No multivalued attributes unless stated.
# 1. Two entities, E1 and E2, related M:N, partial participation on both sides.
TABLES_Q1 = 3
# 2. E1 (one) related 1:N to E2 (many), partial participation.
TABLES_Q2 = 2
# 3. E1 related 1:1 to E2, total participation on both sides.
TABLES_Q3 = 1
# 4. E1 has one multivalued attribute; E1 is related 1:N to E2.
TABLES_Q4 = 3
# 5. E1, E2 and E3. E1-E2 is M:N, E2-E3 is 1:N, E1-E3 is 1:1 with total participation on E1's side only.
TABLES_Q5 = 4

# In a 1:N relationship, the foreign key goes in the table of which side? "one" or "many"
FOREIGN_KEY_SIDE_1_TO_N = "many"
# A 1:1 relationship is a foreign key plus which constraint on it? (an SQL keyword)
ONE_TO_ONE_NEEDS = "UNIQUE"
# True or False: a FOREIGN KEY alone can make sure every county has at least one constituency.
FK_ENFORCES_EVERY_COUNTY_HAS_A_CONSTITUENCY = False
# True or False: NOT NULL on constituencies.county_code makes every constituency belong to a county.
NOT_NULL_ENFORCES_EVERY_CONSTITUENCY_HAS_A_COUNTY = True
