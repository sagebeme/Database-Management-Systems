"""Day 82: a migration runner.

Migrations are .sql files in one folder, named NNN_what_it_does.sql: 001_create_vehicles.sql, 002_add_seats.sql.
The number is the version. They run in version order, each exactly once per database, and the database remembers
which have run in a table:

    schema_migrations (version INT PRIMARY KEY, name TEXT NOT NULL, checksum TEXT NOT NULL,
                       applied_at TIMESTAMPTZ NOT NULL DEFAULT now())

`conn` is a psycopg connection with autocommit=True.
"""

import hashlib
import re
from pathlib import Path

NAME = re.compile(r"^(\d{3})_([a-z0-9_]+)\.sql$")


class MigrationError(Exception):
    """A migration couldn't be applied, or the history doesn't match the files. (Done for you.)"""


def migration_files(folder):
    """(version, name, path) for every .sql file in folder, by version. version is an int and name is the file
    name without the number and .sql: "001_create_vehicles.sql" is (1, "create_vehicles", path).
    Raise MigrationError for a .sql file whose name doesn't fit the pattern, or two files with one version."""
    raise NotImplementedError("write this")


def applied(conn):
    """The versions already applied, as a set. Create schema_migrations first if it isn't there."""
    raise NotImplementedError("write this")


def checksum(path):
    """The SHA-256 of a file's bytes, in hex. (Done for you.)"""
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def migrate(conn, folder):
    """Apply every migration in folder that hasn't been applied, in version order, and return their versions.
    Each runs in its own transaction together with its row in schema_migrations, so a migration is either
    applied and recorded, or neither. If one fails, roll it back, leave the earlier ones applied, and raise
    MigrationError naming the file. Call check_history(conn, folder) before applying anything."""
    raise NotImplementedError("write this")


def check_history(conn, folder):
    """Kata: raise MigrationError if an applied migration's file is missing, or its checksum isn't the one
    recorded when it ran (someone edited history). Called by migrate() before it applies anything."""
    return  # the kata: until you write it, history isn't checked
