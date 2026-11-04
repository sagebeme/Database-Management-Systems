#!/usr/bin/env bash
# Opens the course's MySQL with the settings in .env (or the tools/devdb.sh defaults).
#
#   tools/mysql.sh                      a mysql> prompt
#   tools/mysql.sh shop_db              a prompt inside shop_db
#   tools/mysql.sh shop_db < 3-x.sql    run a file, the way the tests do
#
# Anything after the database name goes straight to the mysql client.
set -euo pipefail
root="$(cd "$(dirname "$0")/.." && pwd)"
[ -f "$root/.env" ] && set -a && . "$root/.env" && set +a
export MYSQL_PWD="${MYSQL_PASSWORD:-}"
exec mysql --no-defaults -h"${MYSQL_HOST:-127.0.0.1}" -P"${MYSQL_PORT:-3307}" -u"${MYSQL_USER:-root}" \
  --default-character-set=utf8mb4 --local-infile=1 "$@"
