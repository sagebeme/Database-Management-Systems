"""Day 29: the chama's records, kept in CSV files the way they were kept in an exercise book.

members.csv        id,name,phone
contributions.csv  member_id,month,amount
"""

import csv
import os
from pathlib import Path

MEMBER_FIELDS = ["id", "name", "phone"]


def read_rows(path):
    """Every row of a CSV file as a dict of strings; [] if the file doesn't exist yet. (Done for you.)"""
    path = Path(path)
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def add_member(path, name, phone):
    """Add a member to members.csv and return their new id.

    Ids are 1, 2, 3, ... (one more than the biggest so far). Create the file, with its header
    row, if it doesn't exist. Two members can't share a phone: raise ValueError if the phone is
    already there."""
    raise NotImplementedError


def find_by_phone(path, phone):
    """The member row (a dict) whose phone matches, or None."""
    raise NotImplementedError


def totals(members_path, contributions_path):
    """Each member's name mapped to the total they've contributed (an int). Members who
    haven't paid anything map to 0. Contributions by unknown member ids are ignored."""
    raise NotImplementedError


def orphans(members_path, contributions_path):
    """Contribution rows (dicts, in file order) whose member_id isn't any member's id."""
    raise NotImplementedError


def rename(path, member_id, new_name):
    """Change one member's name. Raise KeyError if there's no member with that id.

    Rewrite the whole file, but safely: write a new file next to it, then swap it in with
    os.replace, so a crash halfway never leaves a half-written members.csv."""
    raise NotImplementedError


def add_member_locked(path, name, phone):
    """Kata: Two Treasurers. The same as add_member, but safe when many people add members at
    the same moment: no two members may ever get the same id. Hold an exclusive lock on a file
    called members.csv.lock (fcntl.flock) while you read and write."""
    raise NotImplementedError
