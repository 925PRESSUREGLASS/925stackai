#!/usr/bin/env pwsh
$ErrorActionPreference = 'Stop'

# 1. Python env & deps
if (!(Test-Path '.venv')) {
    python -m venv .venv
}
. .\.venv\Scripts\Activate.ps1
pip install --upgrade pip -q
pip install -r requirements.txt -q

# 2. Rebuild vector index
python scripts/rebuild_index.py --input ./docs --store ./memory/vector_store

# 3. Docker Compose stack
docker compose --env-file .env up --build -d

# 4. Run tests
pytest -q

# 5. Wait for Streamlit GUI & open
python scripts/helper/wait_on_port.py 8501
Start-Process http://localhost:8501

Write-Host '✅ 925stackai is up and running.'
