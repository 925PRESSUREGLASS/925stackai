# 925stackai

A new project repository.

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
