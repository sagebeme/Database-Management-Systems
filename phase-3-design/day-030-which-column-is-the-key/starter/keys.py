"""Day 30: keys, found in data and counted on paper."""

from itertools import combinations


def unique_on(rows, columns):
    """True if no two rows (dicts) have the same values in all of `columns` together."""
    raise NotImplementedError


def could_be_keys(rows, columns):
    """Every minimal set of columns that is unique on these rows: the candidate keys, as far
    as this data can tell. Return tuples of column names in the order `columns` lists them,
    smallest sets first, then in the order itertools.combinations produces them. Leave out
    any set that contains a smaller set already found (it's a superkey, not a candidate key)."""
    raise NotImplementedError


def count_superkeys(attributes, candidate_keys):
    """How many superkeys a relation with these attributes has, given ALL its candidate keys.

    A superkey is any set of attributes containing at least one candidate key. Count them
    without listing them: inclusion-exclusion over the candidate keys."""
    raise NotImplementedError


def all_superkeys(attributes, candidate_keys):
    """Kata: Every Superkey. List every superkey as a tuple of attributes in the order
    `attributes` lists them, smallest first, then in itertools.combinations order."""
    raise NotImplementedError
