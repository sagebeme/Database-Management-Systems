"""Day 86: embed or reference? Replace each None."""

# "embed" or "reference"

A_VEHICLES_OWNER_DETAILS = "embed"           # one owner per vehicle, always shown with it
A_ROUTES_LIST_OF_STOPS = "embed"             # a dozen stops, read with the route, rarely changed
A_VEHICLES_TRIPS = "reference"               # grows by dozens a day, forever
DRIVERS_WHO_DRIVE_MANY_VEHICLES = "reference"   # many to many, and a driver's details change in one place
A_BOOKINGS_SEAT_NUMBERS = "embed"            # a few numbers that belong to the booking alone
EVERY_COMMENT_ON_A_POPULAR_ROUTE = "reference"  # thousands, would burst the 16 MB document limit

# The most a single MongoDB document can hold, in megabytes.
DOCUMENT_LIMIT_MB = 16
