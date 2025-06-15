# OracleGit

**OracleGit** is a CLI tool for managing configuration tables in Oracle databases as if they were version-controlled with Git.  
It allows you to take snapshots, compare changes, and generate rollback SQL scripts to safely revert parameter changes.

---

## 📦 Features

- Snapshot creation of parameter tables (`INSERT`, `UPDATE`, `DELETE`)
- Store snapshots as JSON files
- Compare two snapshots (`diff`) using primary key fields
- Generate rollback SQL scripts based on differences
- Delete, inspect and list historical snapshots
- File-system and database-agnostic architecture

---

## ⚙️ Installation

1. Clone the repository:

```bash
git clone https://github.com/your-user/OracleGit.git
cd OracleGit
```

2. (Optional) Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

3. Install the dependencies:

```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the root directory:

```dotenv
ORACLE_USER=your_user
ORACLE_PASSWORD=your_password
ORACLE_DSN=host:port/service_name
```

---

## 🚀 CLI Usage

All commands are available through the main entrypoint:

```bash
python cli/main.py [command]
```

---

### 🔍 Snapshot Commands

#### Create a snapshot of a table

```bash
python cli/main.py snapshot create <table_name>
```

#### List all snapshots for a table

```bash
python cli/main.py snapshot list <table_name>
```

#### Show the contents of a snapshot file

```bash
python cli/main.py snapshot show <path_to_snapshot_file>
```

#### Delete a snapshot file

```bash
python cli/main.py snapshot delete <path_to_snapshot_file>
```

---

### 🧾 Diff Command

Compare two snapshots of a table using key fields:

```bash
python cli/main.py diff <table_name> --from <old_snapshot.json> --to <new_snapshot.json> --keys id
```

---

### 🔁 Rollback Command

Generate SQL to rollback from the current database state to a previous snapshot:

```bash
python cli/main.py rollback <table_name> --to <snapshot_file> --keys id
```

Optional: save SQL to a file

```bash
python cli/main.py rollback <table_name> --to <snapshot_file> --keys id --output rollback_script.sql
```

---

## 🔐 Environment Variables

These must be defined in a `.env` file in the root directory:

| Variable          | Description                |
|------------------|----------------------------|
| `ORACLE_USER`    | Oracle DB username         |
| `ORACLE_PASSWORD`| Oracle DB password         |
| `ORACLE_DSN`     | Oracle DSN (host:port/sid) |

---

## 🧪 Testing

Run unit tests with coverage:

```bash
pytest --cov=core
```

---

## 📁 Project Structure (Simplified)

```
OracleGit/
├── cli/                   # Command-line interface
├── core/                  # Application logic & services
├── adapters/              # Oracle, mock and filesystem
├── config/                # Environment loading
├── tests/                 # Pytest-based tests
├── .env                   # Oracle credentials (not committed)
└── requirements.txt       # Python dependencies
```

---

## 📌 TODO

- Connect to real Oracle DB (already supported via oracledb)
- Snapshot diff visualization improvements
- Integration with Git history?
- Web UI?

---

## 🛠 Built with

- Python 3.12
- `click`, `pytest`, `oracledb`, `dotenv`
- Clean hexagonal architecture
