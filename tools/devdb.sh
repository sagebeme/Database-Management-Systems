#!/usr/bin/env bash
# Starts private copies of MySQL, PostgreSQL, MongoDB and Redis that belong to you, not to the
# system: no sudo, no passwords to set up, and nothing touches a database server you already run.
#
#   tools/devdb.sh up [mysql|postgres|mongo|redis ...]   start them (all four by default)
#   tools/devdb.sh down                                  stop them
#   tools/devdb.sh status                                which ones are running
#   tools/devdb.sh reset                                 stop them and delete their data
#
# They listen on 127.0.0.1 only, on ports that don't clash with the usual ones:
#   MySQL 3307, PostgreSQL 5434, MongoDB 27018, Redis 6380
# and match .env.example, so the tests find them without any configuration.
set -euo pipefail

DATA="${DBMS_DEVDB_DIR:-${XDG_DATA_HOME:-$HOME/.local/share}/dbms-course}"
# Ubuntu's AppArmor profile only lets mysqld write in its own folders and /tmp, so MySQL's data
# goes in /tmp. It starts empty after a reboot, which is fine: every day's tests load their own data.
MYSQL_DATA="${DBMS_MYSQL_DIR:-${TMPDIR:-/tmp}/dbms-course-$(id -u)/mysql}"
MYSQL_PORT=3307 PG_PORT=5434 MONGO_PORT=27018 REDIS_PORT=6380

pg_bin() {
  local dir
  for dir in $(ls -d /usr/lib/postgresql/*/bin 2>/dev/null | sort -V -r) /usr/local/bin /opt/homebrew/bin; do
    [ -x "$dir/pg_ctl" ] && { echo "$dir"; return; }
  done
  command -v pg_ctl >/dev/null && dirname "$(command -v pg_ctl)" && return
  return 1
}

need() { command -v "$1" >/dev/null || { echo "  $2: '$1' isn't installed (see README: Setting up)"; return 1; }; }

wait_for() { # wait_for <seconds> <command...>
  local n=$1; shift
  for _ in $(seq 1 "$n"); do "$@" >/dev/null 2>&1 && return 0; sleep 1; done
  return 1
}

up_mysql() {
  need mysqld MySQL || return 0
  local d="$MYSQL_DATA"
  if [ ! -d "$d/data" ]; then
    mkdir -p "$d"
    mysqld --no-defaults --initialize-insecure --datadir="$d/data" --user="$(whoami)" >"$d/init.log" 2>&1
  fi
  if mysql_up; then echo "  MySQL already running on $MYSQL_PORT"; return; fi
  mysqld --no-defaults --datadir="$d/data" --port=$MYSQL_PORT --bind-address=127.0.0.1 \
    --socket="$d/mysql.sock" --pid-file="$d/mysql.pid" --log-error="$d/error.log" \
    --mysqlx=OFF --local-infile=ON --log-bin-trust-function-creators=ON \
    --character-set-server=utf8mb4 --collation-server=utf8mb4_0900_ai_ci >/dev/null 2>&1 &
  wait_for 60 mysql_up && echo "  MySQL      127.0.0.1:$MYSQL_PORT  user root, no password" \
    || { echo "  MySQL failed to start; see $d/error.log"; return 1; }
}
mysql_up() { mysqladmin --no-defaults -h127.0.0.1 -P$MYSQL_PORT -uroot ping >/dev/null 2>&1; }

up_postgres() {
  local bin; bin=$(pg_bin) || { echo "  PostgreSQL: 'pg_ctl' isn't installed (see README: Setting up)"; return 0; }
  local d="$DATA/postgres"
  if [ ! -d "$d/data" ]; then
    mkdir -p "$d"
    "$bin/initdb" -D "$d/data" -U postgres --auth=trust -E UTF8 --locale=C.UTF-8 >"$d/init.log" 2>&1
  fi
  if pg_up; then echo "  PostgreSQL already running on $PG_PORT"; return; fi
  "$bin/pg_ctl" -D "$d/data" -l "$d/server.log" -w \
    -o "-p $PG_PORT -k $d -c listen_addresses=127.0.0.1" start >/dev/null
  pg_up && echo "  PostgreSQL 127.0.0.1:$PG_PORT  user postgres, no password" \
    || { echo "  PostgreSQL failed to start; see $d/server.log"; return 1; }
}
pg_up() { PGCONNECT_TIMEOUT=3 psql -w -h 127.0.0.1 -p $PG_PORT -U postgres -d postgres -Atc 'select 1' >/dev/null 2>&1; }

up_mongo() {
  need mongod MongoDB || return 0
  local d="$DATA/mongo"
  mkdir -p "$d/data"
  if mongo_up; then echo "  MongoDB already running on $MONGO_PORT"; return; fi
  mongod --dbpath "$d/data" --port $MONGO_PORT --bind_ip 127.0.0.1 --fork \
    --logpath "$d/mongod.log" --pidfilepath "$d/mongod.pid" >/dev/null
  wait_for 30 mongo_up && echo "  MongoDB    127.0.0.1:$MONGO_PORT" \
    || { echo "  MongoDB failed to start; see $d/mongod.log"; return 1; }
}
mongo_up() { mongosh --quiet --port $MONGO_PORT --eval 'db.runCommand({ping:1}).ok' >/dev/null 2>&1; }

up_redis() {
  need redis-server Redis || return 0
  local d="$DATA/redis"
  mkdir -p "$d"
  if redis_up; then echo "  Redis already running on $REDIS_PORT"; return; fi
  redis-server --port $REDIS_PORT --bind 127.0.0.1 --dir "$d" --daemonize yes \
    --pidfile "$d/redis.pid" --logfile "$d/redis.log" --save "" >/dev/null
  wait_for 15 redis_up && echo "  Redis      127.0.0.1:$REDIS_PORT" \
    || { echo "  Redis failed to start; see $d/redis.log"; return 1; }
}
redis_up() { redis-cli -p $REDIS_PORT ping >/dev/null 2>&1; }

down() {
  mysql_up && mysqladmin --no-defaults -h127.0.0.1 -P$MYSQL_PORT -uroot shutdown 2>/dev/null && echo "  MySQL stopped"
  if pg_up; then "$(pg_bin)/pg_ctl" -D "$DATA/postgres/data" -m fast stop >/dev/null && echo "  PostgreSQL stopped"; fi
  mongo_up && { mongosh --quiet --port $MONGO_PORT admin --eval 'db.shutdownServer()' >/dev/null 2>&1 || true; echo "  MongoDB stopped"; }
  redis_up && redis-cli -p $REDIS_PORT shutdown nosave >/dev/null 2>&1; echo "  Redis stopped (if it was running)"
}

status() {
  mysql_up && echo "  MySQL      up   127.0.0.1:$MYSQL_PORT" || echo "  MySQL      down"
  pg_up && echo "  PostgreSQL up   127.0.0.1:$PG_PORT" || echo "  PostgreSQL down"
  mongo_up && echo "  MongoDB    up   127.0.0.1:$MONGO_PORT" || echo "  MongoDB    down"
  redis_up && echo "  Redis      up   127.0.0.1:$REDIS_PORT" || echo "  Redis      down"
}

cmd="${1:-status}"; shift || true
case "$cmd" in
  up)
    targets=("$@"); [ ${#targets[@]} -eq 0 ] && targets=(mysql postgres mongo redis)
    echo "Data lives in $DATA (MySQL's in $MYSQL_DATA)"
    for t in "${targets[@]}"; do "up_$t"; done ;;
  down) down ;;
  status) status ;;
  reset) down; rm -rf "$DATA" "$MYSQL_DATA"; echo "  Deleted $DATA and $MYSQL_DATA" ;;
  *) sed -n '2,12p' "$0"; exit 1 ;;
esac
