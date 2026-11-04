"""Reads Mermaid ER diagrams (the `erDiagram` blocks GitHub draws for you) so tests can check them.

    erDiagram
        CUSTOMER ||--o{ ORDER : places
        CUSTOMER {
            int id PK
            string phone UK "with 254"
        }

Only the crow's-foot symbols are understood (not the word aliases like `one or more`):

    left  right   how many
    |o    o|      zero or one
    ||    ||      exactly one
    }o    o{      zero or more
    }|    |{      one or more

`--` is an identifying relationship (a weak entity's), `..` a non-identifying one.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path

MANY = "N"
_LEFT = {"|o": (0, 1), "||": (1, 1), "}o": (0, MANY), "}|": (1, MANY)}
_RIGHT = {"o|": (0, 1), "||": (1, 1), "o{": (0, MANY), "|{": (1, MANY)}
_NAME = r'(?:"[^"]+"|[A-Za-z_][\w-]*)'
_REL = re.compile(rf"^({_NAME})\s+(\|o|\|\||\}}o|\}}\|)(--|\.\.)(o\||\|\||o\{{|\|\{{)\s+({_NAME})\s*:\s*(.+)$")
_ENTITY_OPEN = re.compile(rf"^({_NAME})\s*\{{$")
_ATTRIBUTE = re.compile(r'^([\w\[\]()-]+)\s+([\w-]+)((?:\s+(?:PK|FK|UK)(?:\s*,\s*(?:PK|FK|UK))*)?)\s*(?:"([^"]*)")?$')


class DiagramError(ValueError):
    """The text isn't a Mermaid ER diagram this reader understands; the message says which line."""


@dataclass
class Attribute:
    type: str
    keys: set[str] = field(default_factory=set)
    comment: str = ""


@dataclass
class Relationship:
    left: str
    right: str
    left_card: tuple  # how many `left` rows go with one `right` row
    right_card: tuple  # how many `right` rows go with one `left` row
    identifying: bool
    label: str


@dataclass
class Diagram:
    entities: dict[str, dict[str, Attribute]] = field(default_factory=dict)
    relationships: list[Relationship] = field(default_factory=list)

    def entity(self, name: str) -> dict[str, Attribute]:
        """The attributes of an entity, looked up ignoring case."""
        for key, attrs in self.entities.items():
            if key.lower() == name.lower():
                return attrs
        raise AssertionError(f"there's no entity called {name}; the diagram has {sorted(self.entities)}")

    def has_entity(self, name: str) -> bool:
        return any(key.lower() == name.lower() for key in self.entities)

    def keys(self, name: str, kind: str = "PK") -> set[str]:
        return {a for a, attr in self.entity(name).items() if kind in attr.keys}

    def between(self, a: str, b: str) -> list[Relationship]:
        a, b = a.lower(), b.lower()
        return [r for r in self.relationships if {r.left.lower(), r.right.lower()} == {a, b} or
                (a == b and r.left.lower() == r.right.lower() == a)]

    def how_many(self, x: str, per: str) -> tuple:
        """(min, max) of `x` rows that go with one `per` row, from the one relationship between them.
        max is 1 or "N"."""
        found = self.between(x, per)
        if len(found) != 1:
            raise AssertionError(f"expected one relationship between {x} and {per}, found {len(found)}")
        r = found[0]
        if r.left.lower() == r.right.lower():
            raise AssertionError("use the relationship itself for an entity related to itself")
        return r.left_card if r.left.lower() == x.lower() else r.right_card


def _unquote(name: str) -> str:
    return name[1:-1] if name.startswith('"') else name


def parse(text: str) -> Diagram:
    lines = [ln.split("%%", 1)[0].strip() for ln in text.splitlines()]
    lines = [ln for ln in lines if ln and not ln.startswith("```")]
    if not lines or lines[0] != "erDiagram":
        raise DiagramError("the diagram must start with a line saying erDiagram")
    diagram = Diagram()
    current: str | None = None
    for number, line in enumerate(lines[1:], 2):
        if current is not None:
            if line == "}":
                current = None
                continue
            m = _ATTRIBUTE.match(line)
            if not m:
                raise DiagramError(f"can't read the attribute line {line!r} (type name [PK|FK|UK] [\"comment\"])")
            keys = {k.strip() for k in m.group(3).replace(",", " ").split()} if m.group(3) else set()
            diagram.entities[current][m.group(2)] = Attribute(m.group(1), keys, m.group(4) or "")
            continue
        m = _ENTITY_OPEN.match(line)
        if m:
            current = _unquote(m.group(1))
            diagram.entities.setdefault(current, {})
            continue
        m = _REL.match(line)
        if m:
            left, right = _unquote(m.group(1)), _unquote(m.group(5))
            diagram.entities.setdefault(left, {})
            diagram.entities.setdefault(right, {})
            diagram.relationships.append(Relationship(
                left, right, _LEFT[m.group(2)], _RIGHT[m.group(4)], m.group(3) == "--",
                _unquote(m.group(6).strip())))
            continue
        if re.fullmatch(_NAME, line):
            diagram.entities.setdefault(_unquote(line), {})
            continue
        raise DiagramError(f"can't read line {line!r}")
    if current is not None:
        raise DiagramError(f"the attribute block for {current} is never closed with }}")
    return diagram


def load(path: Path | str) -> Diagram:
    """Parse a .mmd file, or the first ```mermaid block of a .md file."""
    text = Path(path).read_text(encoding="utf-8")
    block = re.search(r"```mermaid\n(.*?)```", text, re.S)
    return parse(block.group(1) if block else text)
