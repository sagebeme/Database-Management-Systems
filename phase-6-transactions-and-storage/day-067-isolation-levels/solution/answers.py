"""Day 67: isolation levels. Replace each None.

The SQL standard's table: for each level, the set of anomalies it ALLOWS, from
{"dirty read", "non-repeatable read", "phantom"}.
"""

STANDARD_ALLOWS = {
    "READ UNCOMMITTED": {"dirty read", "non-repeatable read", "phantom"},
    "READ COMMITTED": {"non-repeatable read", "phantom"},
    "REPEATABLE READ": {"phantom"},
    "SERIALIZABLE": set(),
}

# Each engine's default level, as one of the four strings above.
MYSQL_DEFAULT = "REPEATABLE READ"
POSTGRES_DEFAULT = "READ COMMITTED"

# True or False, from what your experiments showed.
POSTGRES_EVER_SHOWS_A_DIRTY_READ = False
MYSQL_REPEATABLE_READ_SHOWS_PHANTOMS_TO_A_PLAIN_SELECT = False
MYSQL_SERIALIZABLE_MAKES_WRITERS_WAIT_FOR_READERS = True
