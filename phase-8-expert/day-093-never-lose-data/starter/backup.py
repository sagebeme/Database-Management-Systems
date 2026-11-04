"""Day 93: backups you've actually restored.

The Postgres command-line tools run with the course's connection settings (from .env or the defaults), through
tool() and conn_args(), which are done for you.
"""

import glob
import os
import shutil
import subprocess
from datetime import date  # noqa: F401  (keep() works with dates)

from coursekit import setting


def tool(name):
    """The path of a Postgres program (pg_dump, pg_restore, createdb, ...), from the newest version installed, so it
    matches a new server. (Done for you.)"""
    for folder in sorted(glob.glob("/usr/lib/postgresql/*/bin"), key=lambda p: int(p.split("/")[-2]), reverse=True):
        path = os.path.join(folder, name)
        if os.access(path, os.X_OK):
            return path
    found = shutil.which(name)
    if not found:
        raise FileNotFoundError(f"{name} isn't installed")
    return found


def conn_args():
    """The -h -p -U arguments every Postgres program needs here. (Done for you.)"""
    return ["-h", setting("PGHOST"), "-p", setting("PGPORT"), "-U", setting("PGUSER"), "-w"]


def run(args):
    """Run a program; raise RuntimeError with its error output if it fails. (Done for you.)"""
    env = {**os.environ, "PGPASSWORD": setting("PGPASSWORD")}
    proc = subprocess.run(args, capture_output=True, text=True, env=env)
    if proc.returncode != 0:
        raise RuntimeError(proc.stderr.strip() or f"{args[0]} failed")
    return proc.stdout


def dump(database, path):
    """Back up the whole database to the file path with pg_dump, in its custom format (-Fc)."""
    raise NotImplementedError("write this")


def restore(path, new_database):
    """Make a new, empty database called new_database (createdb) and restore the backup at path into it
    (pg_restore). RuntimeError if new_database already exists: a restore must never land on top of live data."""
    raise NotImplementedError("write this")


def fingerprint(conn, table):
    """(rows, checksum) for a table: its row count and the md5 of all its rows as text, in primary-key order
    (SELECT md5(string_agg(t::text, ',' ORDER BY id)) FROM table AS t). table is one of the SACCO's tables; check it
    against the database's own list of tables before putting it into SQL."""
    raise NotImplementedError("write this")


def differences(conn_a, conn_b, tables):
    """The tables whose fingerprints differ between two databases, in the order given: how you prove a restore
    worked."""
    raise NotImplementedError("write this")


def keep(backups, today):
    """Kata: grandfather-father-son. backups is a set of dates that have a nightly backup. Keep (return the set of):
    every backup from the last 7 days (today - 6 to today); the Sunday backups from the last 4 weeks (today - 27
    to today); and the backups from the 1st of the month for the last 12 months (today - 364 to today). Everything
    else can be deleted."""
    raise NotImplementedError("write this")
