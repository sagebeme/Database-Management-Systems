"""Day 67 kata: the level's own test.

Run on a database loaded with setup.sql. Use the helpers in levels.py (import them).
"""

from levels import begin, short_waits, blocked, read_one, ACCOUNT  # noqa: F401

import pymysql
import psycopg


def write_skew(connect, engine, level):
    """Write skew. The ward's rule: at least one doctor must be on call. Dr Achieng (connection A) and
    Dr Barasa (B) both want the night off. Each starts a transaction at `level` and counts the doctors on call
    (2). Seeing 2, each takes themselves off call: A updates her row, then B updates his (either may be blocked
    or refused). Then A commits, then B. A blocked or refused statement or commit rolls that transaction back.
    Return how many doctors are on call at the end (counted with a fresh connection)."""
    raise NotImplementedError("write this")
