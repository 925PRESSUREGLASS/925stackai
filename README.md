# 925stackai

A new project repository.

# Wire-up Branch (wireup-1.1)

This branch wires together the core quoting pipeline (CLI → prompt manager → quoting agent) and adds
stubs for future specification and evaluation modules. No new features are introduced.

## Quick Start

1. Copy `.env.example` to `.env` and fill in any API keys.
2. Run the launcher for your platform:

```bash
# Linux/macOS/WSL
./scripts/run_all.sh

# PowerShell Core
pwsh scripts/run_all.ps1

# Windows CMD
run_all.bat
```

The script sets up a Python virtual environment, rebuilds the vector index from
`docs/`, starts the Docker Compose stack, runs the tests and opens the
Streamlit GUI at <http://localhost:8501>.
