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
    rows = read_rows(path)
    if any(r["phone"] == phone for r in rows):
        raise ValueError(f"{phone} already belongs to a member")
    new_id = max((int(r["id"]) for r in rows), default=0) + 1
    is_new = not Path(path).exists()
    with open(path, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=MEMBER_FIELDS)
        if is_new:
            writer.writeheader()
        writer.writerow({"id": new_id, "name": name, "phone": phone})
    return new_id


def find_by_phone(path, phone):
    """The member row (a dict) whose phone matches, or None."""
    for row in read_rows(path):
        if row["phone"] == phone:
            return row
    return None


def totals(members_path, contributions_path):
    """Each member's name mapped to the total they've contributed (an int). Members who
    haven't paid anything map to 0. Contributions by unknown member ids are ignored."""
    names = {r["id"]: r["name"] for r in read_rows(members_path)}
    result = {name: 0 for name in names.values()}
    for c in read_rows(contributions_path):
        if c["member_id"] in names:
            result[names[c["member_id"]]] += int(c["amount"])
    return result


def orphans(members_path, contributions_path):
    """Contribution rows (dicts, in file order) whose member_id isn't any member's id."""
    ids = {r["id"] for r in read_rows(members_path)}
    return [c for c in read_rows(contributions_path) if c["member_id"] not in ids]


def rename(path, member_id, new_name):
    """Change one member's name. Raise KeyError if there's no member with that id.

    Rewrite the whole file, but safely: write a new file next to it, then swap it in with
    os.replace, so a crash halfway never leaves a half-written members.csv."""
    rows = read_rows(path)
    for row in rows:
        if row["id"] == str(member_id):
            row["name"] = new_name
            break
    else:
        raise KeyError(member_id)
    temp = Path(str(path) + ".tmp")
    with temp.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=MEMBER_FIELDS)
        writer.writeheader()
        writer.writerows(rows)
    os.replace(temp, path)


def add_member_locked(path, name, phone):
    """Kata: Two Treasurers. The same as add_member, but safe when many people add members at
    the same moment: no two members may ever get the same id. Hold an exclusive lock on a file
    called members.csv.lock (fcntl.flock) while you read and write."""
    import fcntl
    with open(str(path) + ".lock", "w") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        try:
            return add_member(path, name, phone)
        finally:
            fcntl.flock(lock, fcntl.LOCK_UN)
