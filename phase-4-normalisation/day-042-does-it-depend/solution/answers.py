"""Day 42: functional dependencies. Replace each None."""

# True or False
AB_TO_A_IS_TRIVIAL = True
A_TO_AB_IS_TRIVIAL = False
IF_A_IS_A_KEY_THEN_A_DETERMINES_EVERY_ATTRIBUTE = True
SAMPLE_DATA_CAN_PROVE_AN_FD_HOLDS = False
SAMPLE_DATA_CAN_PROVE_AN_FD_FAILS = True
IF_A_TO_B_HOLDS_THEN_B_TO_A_HOLDS = False

# In trips, which should hold as a rule of the business? "yes" or "no"
PLATE_DETERMINES_SACCO = "yes"     # a vehicle belongs to one sacco
DRIVER_DETERMINES_PLATE = "no"    # Otieno drove KDA 101A one day and KDC 303C another
