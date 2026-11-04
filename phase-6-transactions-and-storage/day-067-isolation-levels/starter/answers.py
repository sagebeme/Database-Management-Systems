"""Day 67: isolation levels. Replace each None.

The SQL standard's table: for each level, the set of anomalies it ALLOWS, from
{"dirty read", "non-repeatable read", "phantom"}.
"""

STANDARD_ALLOWS = {
    "READ UNCOMMITTED": None,
    "READ COMMITTED": None,
    "REPEATABLE READ": None,
    "SERIALIZABLE": None,
}

# Each engine's default level, as one of the four strings above.
MYSQL_DEFAULT = None
POSTGRES_DEFAULT = None

# True or False, from what your experiments showed.
POSTGRES_EVER_SHOWS_A_DIRTY_READ = None
MYSQL_REPEATABLE_READ_SHOWS_PHANTOMS_TO_A_PLAIN_SELECT = None
MYSQL_SERIALIZABLE_MAKES_WRITERS_WAIT_FOR_READERS = None
