
OracleGit is a lightweight version control system for configuration tables in Oracle databases — inspired by Git.

It allows you to create snapshots of parameter tables, track differences between versions, and restore previous states — especially useful in environments where changes are made directly using SQL `INSERT`, `UPDATE`, and `DELETE`.

---

## 🚀 Key Features

- Create timestamped snapshots of any configuration table
- Compare differences between two snapshots (`diff`)
- Roll back to a previous state (`rollback`)
- Modular and extensible architecture (Hexagonal / Ports & Adapters)
- Designed to integrate with Oracle DB (mock connector provided)

---


## ⚙️ Setup Instructions

### 1. Clone the repository

git clone https://github.com/dgalachesoriano/OracleGit.git
cd OracleGit
2. Create a virtual environment

python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

3. Install dependencies
pip install -r requirements.txt
🧪 Run Tests
Run all tests with coverage report:

pytest --cov=core/application --cov-report=term-missing
Or use the Makefile:


make test
make coverage
🧹 Pre-commit Hooks
To ensure code quality and consistency, install pre-commit:


pre-commit install
It will automatically run tools like black, flake8, and isort before each commit.

✅ CI/CD
GitHub Actions automatically runs tests and coverage on:

Every push to master

Every pull request targeting master

You can see workflows in the Actions tab.

🗺️ Roadmap
✅ Snapshot creation and storage (mock-based)

✅ Diff service for comparing table states

✅ Rollback to previous snapshot

⏳ Oracle database connector (real)

⏳ CLI interface (e.g., oraclegit snapshot create <table_name>)

⏳ Public REST API for integration

⏳ Snapshot metadata search & filtering

⏳ Audit logging and change history viewer

👤 Author
Created by David Galache
License: MIT

⚠️ This is a personal project built for educational and professional growth. Not yet production-ready.