# Doing the course on Windows

**Short version: run the course inside WSL (Ubuntu on Windows), not in PowerShell or Command Prompt.** It takes about 20 minutes to set up, once, and then every command in every README works exactly as written.

## Why not plain Windows?

- The helper scripts (`tools/devdb.sh`, `tools/mysql.sh`, `tools/psql.sh`) are Bash scripts.
- The READMEs feed SQL files to the database with `<`, as in `tools/mysql.sh duka < setup.sql`. PowerShell doesn't support `<` at all ("The '<' operator is reserved for future use").
- The tests run the same `mysql`, `psql` and `mongosh` programs you do, and expect Linux versions of them.

WSL gives you a real Ubuntu inside Windows. It isn't a virtual machine you have to manage, and it's what most backend teams on Windows use anyway. Your editor stays on Windows.

## 1. Install WSL and Ubuntu

Open **PowerShell as Administrator** (right-click the Start button, then "Terminal (Admin)") and run:

```powershell
wsl --install -d Ubuntu-24.04
```

Restart when it asks. An **Ubuntu** window opens and asks you to choose a Linux username and password. That password is for `sudo`; you'll need it in a minute.

From now on, everything happens in that **Ubuntu** terminal (find it in the Start menu), not in PowerShell.

## 2. Install the tools

In the Ubuntu terminal:

```bash
sudo apt update
sudo apt install -y git python3-venv mysql-server mysql-client redis-server

# PostgreSQL 17 (Ubuntu 24.04's own package is 16, which is too old for the course's psql commands)
sudo apt install -y postgresql-common
sudo /usr/share/postgresql-common/pgdg/apt.postgresql.org.sh -y
sudo apt install -y postgresql-17
```

**MongoDB and mongosh** (Phase 7) come from MongoDB's own package site. Follow "Install MongoDB Community Edition on Ubuntu" for **Ubuntu 24.04 (Noble)**: https://www.mongodb.com/docs/manual/tutorial/install-mongodb-on-ubuntu/. It installs both the server (`mongod`) and the shell (`mongosh`). Don't install `mongosh` with `npm`: that build crashes when a script is piped into it, and the course pipes scripts in.

You can leave MongoDB until Day 83 if you want to get started.

## 3. Get the course, inside Linux

Clone it into your **Linux home folder**, not into `C:\Users\...`:

```bash
cd ~
git clone https://github.com/sagebeme/Database-Management-Systems.git
cd Database-Management-Systems
python3 -m venv .venv && . .venv/bin/activate
pip install -r requirements.txt
tools/devdb.sh up
pytest phase-1-first-queries/day-001-hello-mysql
```

Why the Linux home folder? Windows drives show up in Ubuntu as `/mnt/c/...`, and working from there is slow, and loses the "this file can be run" flag on the scripts (`Permission denied`). Keep the course in `~` and open it from Windows instead (next step).

Every time you open a new Ubuntu terminal, go back in and switch on the Python environment:

```bash
cd ~/Database-Management-Systems && . .venv/bin/activate
tools/devdb.sh up        # after a restart: the databases don't start on their own
```

## 4. Edit with VS Code

Install VS Code on Windows, then its **WSL** extension. In the Ubuntu terminal, inside the course folder:

```bash
code .
```

VS Code opens on Windows, editing the files in Linux, and its terminal (`` Ctrl+` ``) is an Ubuntu terminal already in the right folder.

You can also reach the files from File Explorer at `\\wsl$\Ubuntu-24.04\home\<your username>\Database-Management-Systems`.

## 5. Line endings: LF, not CRLF

Windows ends lines with two characters (CRLF), Linux with one (LF). The repository forces LF for every file it gives you, but a Windows editor can slip CRLF back in when you save. Then a script fails with:

```
$'\r': command not found
```

- In VS Code, look at the bottom-right corner: if it says **CRLF**, click it and choose **LF**. To make LF the default, add `"files.eol": "\n"` to your settings.
- To fix a file from Ubuntu: `sed -i 's/\r$//' path/to/file`.
- Don't clone with Git for Windows and then open the folder from Ubuntu. Clone in Ubuntu (step 3).

## Rather use Docker?

If you already have **Docker Desktop** with WSL integration switched on, it can run the four databases instead of `tools/devdb.sh`. In the Ubuntu terminal:

```bash
docker compose up -d     # MySQL 8.4, PostgreSQL 17, MongoDB 7 and Redis 8, on the course's ports
```

You still need the client programs in Ubuntu, because the tests run them: `sudo apt install -y mysql-client redis-tools`, PostgreSQL's client with `sudo apt install -y postgresql-client-17` (after the PGDG lines in step 2), and `mongosh` from MongoDB's site. Use one or the other: `tools/devdb.sh up` and `docker compose up` both want the same ports.

## When something goes wrong

| You see | It means | Do this |
|---|---|---|
| `The '<' operator is reserved for future use` | you're in PowerShell | open the Ubuntu terminal |
| `$'\r': command not found` | a file got Windows line endings | step 5 |
| `Permission denied` running `tools/...` | the course is under `/mnt/c` | clone it into `~` (step 3) |
| tests are **skipped** with "isn't available" | the databases aren't running | `tools/devdb.sh up` (or `docker compose up -d`) |
| `\l` fails with `column d.daticulocale does not exist` | your `psql` is older than the server | install `postgresql-17` (step 2) |
| `mongosh: command not found` | MongoDB's shell isn't installed | step 2 |
| `pytest: command not found` | the Python environment is off | `. .venv/bin/activate` |
