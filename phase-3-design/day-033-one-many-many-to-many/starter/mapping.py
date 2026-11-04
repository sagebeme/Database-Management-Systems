"""Day 33: from ER diagrams to tables."""

from coursekit import er


def min_tables(entities, relationships, multivalued=0):
    """The fewest tables needed for an ER diagram, by the usual rules.

    entities       names of the entity sets (strong or weak): each needs a table
    relationships  dicts like {"a": "E1", "b": "E2", "ratio": "1:N", "total_a": False, "total_b": True}
                   ratio is "1:1", "1:N" (a is the one side) or "M:N"; total_x says whether every
                   x must take part
    multivalued    how many multivalued attributes there are: each needs a table

    Rules: an M:N relationship needs its own table. A 1:N relationship needs none (a foreign key
    on the N side). A 1:1 relationship needs none, and if BOTH sides are total, the two entities
    can share one table, which saves a table."""
    raise NotImplementedError


def describe(path):
    """Kata: Read the Diagram. Turn every relationship in a Mermaid ER file into two
    sentences, in the order the relationships appear: first from the left entity's side, then
    from the right's:

        CUSTOMER ||--o{ ORDER : places   ->   "Each CUSTOMER goes with zero or more ORDER."
                                              "Each ORDER goes with exactly one CUSTOMER."

    The phrases are "zero or one", "exactly one", "zero or more" and "one or more".
    Use er.load(path); each relationship has .left, .right, .left_card and .right_card,
    where a card is (min, max) and max is 1 or er.MANY."""
    raise NotImplementedError
