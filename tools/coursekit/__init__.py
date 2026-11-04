"""Helpers the day tests use to talk to real databases.

SQL files run through the real command-line clients (`mysql`, `psql`, `mongosh`), exactly the way
you run them yourself:

    mysql -h127.0.0.1 -P3307 -uroot my_db < 3-list_tables.sql

so a file that works in the tests works at your prompt too, `DELIMITER` lines and all.

Settings come from environment variables, then from a `.env` file at the repository root, then
from defaults that match `tools/devdb.sh`. See `.env.example`.
"""

from __future__ import annotations

import importlib.util
import os
import re
import secrets
import shutil
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path
from types import ModuleType

ROOT = Path(__file__).resolve().parents[2]

DEFAULTS = {
    "MYSQL_HOST": "127.0.0.1",
    "MYSQL_PORT": "3307",
    "MYSQL_USER": "root",
    "MYSQL_PASSWORD": "",
    "PGHOST": "127.0.0.1",
    "PGPORT": "5434",
    "PGUSER": "postgres",
    "PGPASSWORD": "",
    "MONGO_URL": "mongodb://127.0.0.1:27018",
    "REDIS_URL": "redis://127.0.0.1:6380/0",
}


def _read_dotenv(path: Path) -> dict[str, str]:
    values: dict[str, str] = {}
    if not path.is_file():
        return values
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        value = value.strip()
        if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
            value = value[1:-1]
        values[key.strip()] = value
    return values


def setting(name: str) -> str:
    """An environment variable, else the .env value, else the course default."""
    if name in os.environ:
        return os.environ[name]
    return _read_dotenv(ROOT / ".env").get(name, DEFAULTS.get(name, ""))


class DatabaseUnavailable(RuntimeError):
    """The server isn't running or the client program isn't installed."""


@dataclass
class Result:
    """What a client printed. `rows` and `columns` describe the last result set."""

    stdout: str
    stderr: str
    returncode: int
    columns: list[str] = field(default_factory=list)
    rows: list[tuple[str, ...]] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return self.returncode == 0

    def column(self, name_or_index: str | int = 0) -> list[str]:
        index = name_or_index if isinstance(name_or_index, int) else self.columns.index(name_or_index)
        return [row[index] for row in self.rows]

    def check(self) -> "Result":
        """Raise with the client's error message if the file failed."""
        if not self.ok:
            raise AssertionError(f"the SQL failed:\n{self.stderr.strip() or self.stdout.strip()}")
        return self


_MYSQL_ESCAPES = {"\\t": "\t", "\\n": "\n", "\\\\": "\\", "\\0": "\0"}


def _unescape_mysql(value: str) -> str:
    return re.sub(r"\\[tn\\0]", lambda m: _MYSQL_ESCAPES[m.group(0)], value)


def _parse_tsv(text: str, unescape=lambda v: v) -> tuple[list[str], list[tuple[str, ...]]]:
    lines = [line for line in text.split("\n") if line != ""]
    if not lines:
        return [], []
    columns = [unescape(c) for c in lines[0].split("\t")]
    rows = [tuple(unescape(v) for v in line.split("\t")) for line in lines[1:]]
    return columns, rows


def _run(argv: list[str], sql: str, env: dict[str, str] | None = None, timeout: int = 60) -> subprocess.CompletedProcess:
    if shutil.which(argv[0]) is None:
        raise DatabaseUnavailable(f"'{argv[0]}' isn't installed")
    return subprocess.run(
        argv, input=sql, capture_output=True, text=True, encoding="utf-8",
        env={**os.environ, **(env or {})}, timeout=timeout,
    )


class MySQL:
    """Runs SQL through the `mysql` client against one database (or none)."""

    def __init__(self, database: str | None = None, user: str | None = None, password: str | None = None):
        self.database = database
        self.user = user or setting("MYSQL_USER")
        self.password = setting("MYSQL_PASSWORD") if password is None else password

    def _argv(self, database: str | None, raw: bool = False) -> list[str]:
        argv = ["mysql", "--no-defaults", f"-h{setting('MYSQL_HOST')}", f"-P{setting('MYSQL_PORT')}",
                f"-u{self.user}", "--batch", "--default-character-set=utf8mb4", "--local-infile=1"]
        if raw:
            argv.append("--raw")
        if database:
            argv.append(database)
        return argv

    def run(self, sql: str, database: str | None = "", stdin_name: str = "<sql>") -> Result:
        db = self.database if database == "" else database
        proc = _run(self._argv(db), sql, env={"MYSQL_PWD": self.password})
        if proc.returncode != 0 and "Can't connect" in proc.stderr:
            raise DatabaseUnavailable(proc.stderr.strip())
        columns, rows = _parse_tsv(proc.stdout, _unescape_mysql)
        return Result(proc.stdout, proc.stderr, proc.returncode, columns, rows)

    def run_file(self, path: Path | str, database: str | None = "") -> Result:
        return self.run(Path(path).read_text(encoding="utf-8"), database)

    def ping(self) -> None:
        self.run("SELECT 1;", database=None).check()


class Postgres:
    """Runs SQL through `psql` against one database."""

    def __init__(self, database: str = "postgres", user: str | None = None, password: str | None = None):
        self.database = database
        self.user = user or setting("PGUSER")
        self.password = setting("PGPASSWORD") if password is None else password

    def run(self, sql: str, database: str | None = None) -> Result:
        argv = ["psql", "-X", "-w", "-q", "-v", "ON_ERROR_STOP=1", "-A", "-F", "\t", "-P", "footer=off",
                "-P", "null=NULL", "-h", setting("PGHOST"), "-p", setting("PGPORT"), "-U", self.user,
                "-d", database or self.database]
        proc = _run(argv, sql, env={"PGPASSWORD": self.password, "PGCONNECT_TIMEOUT": "5"})
        if proc.returncode != 0 and ("Connection refused" in proc.stderr or "could not connect" in proc.stderr):
            raise DatabaseUnavailable(proc.stderr.strip())
        columns, rows = _parse_tsv(proc.stdout)
        return Result(proc.stdout, proc.stderr, proc.returncode, columns, rows)

    def run_file(self, path: Path | str, database: str | None = None) -> Result:
        return self.run(Path(path).read_text(encoding="utf-8"), database)

    def ping(self) -> None:
        self.run("SELECT 1;").check()


class Mongo:
    """Runs a mongosh script against one database, the way `cat 2-insert | mongosh my_db` does."""

    def __init__(self, database: str):
        self.database = database

    def run(self, script: str) -> Result:
        url = setting("MONGO_URL").rstrip("/") + "/" + self.database
        proc = _run(["mongosh", "--quiet", "--norc", url], script)
        if proc.returncode != 0 and ("ECONNREFUSED" in proc.stderr + proc.stdout):
            raise DatabaseUnavailable((proc.stderr or proc.stdout).strip())
        return Result(proc.stdout, proc.stderr, proc.returncode)

    def run_file(self, path: Path | str) -> Result:
        return self.run(Path(path).read_text(encoding="utf-8"))


def new_name(prefix: str = "dbms") -> str:
    """A database name nobody else is using: dbms_t_3f9a1c."""
    return f"{prefix}_t_{secrets.token_hex(3)}"


def load_module(path: Path | str, name: str | None = None) -> ModuleType:
    """Import a learner's .py file by path, fresh each time."""
    path = Path(path)
    name = name or f"_dbms_{path.parent.parent.name}_{path.parent.name}_{path.stem}".replace("-", "_")
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise ImportError(f"can't import {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    sys.path.insert(0, str(path.parent))
    try:
        spec.loader.exec_module(module)
    finally:
        sys.path.remove(str(path.parent))
    return module
