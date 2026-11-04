"""Day 31: which kind of integrity does each mistake break?

Answer each with one of: "domain", "entity", "key", "referential".
"""

RIDER_AGED_TWELVE = "domain"
RIDER_WITH_NULL_ID = "entity"
TWO_RIDERS_SAME_LICENCE = "key"
BIKE_OF_RIDER_99_WHO_DOES_NOT_EXIST = "referential"
TRIP_WITH_FARE_MINUS_50 = "domain"
DELETING_A_RIDER_WHOSE_BIKES_STILL_POINT_AT_THEM = "referential"
ENGINE_CC_OF_TEXT_FAST = "domain"
