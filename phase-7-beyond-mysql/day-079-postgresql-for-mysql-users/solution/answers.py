"""Day 79: Postgres for MySQL users. Replace each None with a string."""

# The psql command that lists the tables (like SHOW TABLES).
LIST_TABLES = r"\dt"
# The psql command that describes the table routes (like DESCRIBE routes).
DESCRIBE_ROUTES = r"\d routes"
# The psql command that lists the databases (like SHOW DATABASES).
LIST_DATABASES = r"\l"
# The psql command that connects to the database matatu (like USE matatu).
USE_MATATU = r"\c matatu"
# The psql command that quits.
QUIT = r"\q"
