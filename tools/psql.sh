#!/usr/bin/env bash
# Opens the course's PostgreSQL with the settings in .env (or the tools/devdb.sh defaults).
#
#   tools/psql.sh                       a postgres=# prompt
#   tools/psql.sh shop_db < 3-x.sql     run a file in shop_db
set -euo pipefail
root="$(cd "$(dirname "$0")/.." && pwd)"
[ -f "$root/.env" ] && set -a && . "$root/.env" && set +a
db="${1:-postgres}"; [ $# -gt 0 ] && shift
exec psql -X -h "${PGHOST:-127.0.0.1}" -p "${PGPORT:-5434}" -U "${PGUSER:-postgres}" -d "$db" "$@"
