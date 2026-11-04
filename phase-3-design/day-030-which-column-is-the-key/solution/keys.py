"""Day 30: keys, found in data and counted on paper."""

from itertools import combinations


def unique_on(rows, columns):
    """True if no two rows (dicts) have the same values in all of `columns` together."""
    seen = set()
    for row in rows:
        value = tuple(row[c] for c in columns)
        if value in seen:
            return False
        seen.add(value)
    return True


def could_be_keys(rows, columns):
    """Every minimal set of columns that is unique on these rows: the candidate keys, as far
    as this data can tell. Return tuples of column names in the order `columns` lists them,
    smallest sets first, then in the order itertools.combinations produces them. Leave out
    any set that contains a smaller set already found (it's a superkey, not a candidate key)."""
    found = []
    for size in range(1, len(columns) + 1):
        for combo in combinations(columns, size):
            if any(set(key) <= set(combo) for key in found):
                continue
            if unique_on(rows, combo):
                found.append(combo)
    return found


def count_superkeys(attributes, candidate_keys):
    """How many superkeys a relation with these attributes has, given ALL its candidate keys.

    A superkey is any set of attributes containing at least one candidate key. Count them
    without listing them: inclusion-exclusion over the candidate keys."""
    attributes = set(attributes)
    total = 0
    for size in range(1, len(candidate_keys) + 1):
        for chosen in combinations(candidate_keys, size):
            union = set().union(*map(set, chosen))
            total += (-1) ** (size + 1) * 2 ** len(attributes - union)
    return total


def all_superkeys(attributes, candidate_keys):
    """Kata: Every Superkey. List every superkey as a tuple of attributes in the order
    `attributes` lists them, smallest first, then in itertools.combinations order."""
    keys = [set(k) for k in candidate_keys]
    return [combo for size in range(1, len(attributes) + 1)
            for combo in combinations(attributes, size)
            if any(k <= set(combo) for k in keys)]
