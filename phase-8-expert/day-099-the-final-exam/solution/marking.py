"""Day 99 kata: mark a paper the way GATE does."""

from fractions import Fraction


def same(kind: str, given, correct) -> bool:
    """Done for you: is an answer right? MSQ answers compare as sets of letters, the rest as values."""
    if kind == "MSQ":
        return {str(x).strip().upper() for x in given} == {str(x).strip().upper() for x in correct}
    if kind == "MCQ":
        return str(given).strip().upper() == str(correct).strip().upper()
    return given == correct


def gate_score(paper: dict, given: dict) -> Fraction:
    """paper maps a question number to (kind, marks, correct answer); given maps question numbers to answers,
    with None or a missing number for a blank. A right answer earns its marks. A wrong MCQ loses a third of
    its marks; a wrong MSQ or NAT, or a blank, costs nothing. Returns an exact Fraction."""
    score = Fraction(0)
    for number, (kind, marks, correct) in paper.items():
        answer = given.get(number)
        if answer is None:
            continue
        if same(kind, answer, correct):
            score += marks
        elif kind == "MCQ":
            score -= Fraction(marks, 3)
    return score
