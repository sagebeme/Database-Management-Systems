#!/usr/bin/env python3
"""Proves the course works.

For every day (or only the days you name):

1. its folder has a README.md, a test_day.py, and starter/ and solution/ folders holding the
   same file names;
2. every test passes against solution/, with nothing skipped;
3. every test fails against the untouched starter/, so the tests really check the work
   (a test marked @pytest.mark.passes_on_starter is allowed to pass).

    python tools/verify.py            # every day
    python tools/verify.py 1 2 14     # just those days

Needs the databases running (tools/devdb.sh up). Exits non-zero if anything is wrong.
"""

from __future__ import annotations

import json
import os
import re
import subprocess
import sys
import tempfile
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
IGNORED = {"__pycache__", ".pytest_cache", ".DS_Store"}


def day_dirs(selected: set[int]) -> list[Path]:
    days = []
    for path in sorted(ROOT.glob("phase-*/day-*")):
        match = re.match(r"day-(\d{3})-", path.name)
        if path.is_dir() and match and (not selected or int(match.group(1)) in selected):
            days.append(path)
    return days


def files_in(folder: Path) -> set[str]:
    return {
        str(p.relative_to(folder)) for p in folder.rglob("*")
        if p.is_file() and not (set(p.relative_to(folder).parts) & IGNORED)
    }


def check_layout(day: Path) -> list[str]:
    problems = []
    for needed in ("README.md", "test_day.py", "starter", "solution"):
        if not (day / needed).exists():
            problems.append(f"missing {needed}")
    if (day / "starter").is_dir() and (day / "solution").is_dir():
        starter, solution = files_in(day / "starter"), files_in(day / "solution")
        if starter != solution:
            only_s = sorted(starter - solution)
            only_sol = sorted(solution - starter)
            problems.append(f"starter/ and solution/ differ: only in starter {only_s}, only in solution {only_sol}")
    readme = day / "README.md"
    if readme.is_file():
        text = readme.read_text(encoding="utf-8")
        for heading in ("## The brief", "## What you'll use", "## Steps", "## When you're stuck"):
            if heading not in text:
                problems.append(f"README.md has no '{heading}' section")
    return problems


def run_pytest(days: list[Path], which: str) -> dict[str, list[dict]]:
    with tempfile.NamedTemporaryFile("w+", suffix=".jsonl", delete=False) as report:
        report_path = report.name
    env = {**os.environ, "DBMS_TARGET": which, "DBMS_REQUIRE": "1", "DBMS_REPORT": report_path}
    subprocess.run(
        [sys.executable, "-m", "pytest", "-q", "-p", "no:randomly", "--no-header", "-rN", "--tb=no",
         *[str(d / "test_day.py") for d in days]],
        cwd=ROOT, env=env, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, text=True,
    )
    by_day: dict[str, list[dict]] = defaultdict(list)
    with open(report_path, encoding="utf-8") as f:
        for line in f:
            entry = json.loads(line)
            by_day[entry["nodeid"].split("/test_day.py")[0]].append(entry)
    os.unlink(report_path)
    return by_day


def main(argv: list[str]) -> int:
    selected = {int(a) for a in argv if a.isdigit()}
    days = day_dirs(selected)
    if not days:
        print("No days found.")
        return 1

    problems: dict[str, list[str]] = defaultdict(list)
    for day in days:
        problems[str(day.relative_to(ROOT))].extend(check_layout(day))

    testable = [d for d in days if (d / "test_day.py").is_file()]
    solution = run_pytest(testable, "solution")
    starter = run_pytest(testable, "starter")

    total_tests = 0
    for day in testable:
        key = str(day.relative_to(ROOT))
        sol = solution.get(key, [])
        if not sol:
            problems[key].append("no tests ran against solution/ (does test_day.py import?)")
        total_tests += len(sol)
        for t in sol:
            if t["outcome"] != "passed":
                problems[key].append(f"solution {t['outcome']}: {t['nodeid'].split('::', 1)[1]}")
        for t in starter.get(key, []):
            if t["outcome"] == "passed" and not t["passes_on_starter"]:
                problems[key].append(f"starter passes (so the test proves nothing): {t['nodeid'].split('::', 1)[1]}")
            if t["outcome"] == "skipped":
                problems[key].append(f"starter skipped: {t['nodeid'].split('::', 1)[1]}")

    bad = {k: v for k, v in problems.items() if v}
    for day in days:
        key = str(day.relative_to(ROOT))
        print(("FAIL " if key in bad else "ok   ") + key)
        for p in bad.get(key, []):
            print(f"       {p}")
    print(f"\n{len(days)} days, {total_tests} tests, {len(bad)} with problems.")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
