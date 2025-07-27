@echo off
REM run_all.bat - Unified Windows launcher

REM 1. Python env & deps
if not exist .venv (
    python -m venv .venv
)
call .venv\Scripts\activate.bat
pip install --upgrade pip >nul
pip install -r requirements.txt >nul

REM 2. Rebuild vector index
python scripts\rebuild_index.py --input docs --store memory\vector_store

REM 3. Docker Compose stack
docker compose --env-file .env up --build -d

REM 4. Run tests
pytest -q

REM 5. Wait and open Streamlit GUI
python scripts\helper\wait_on_port.py 8501
start http://localhost:8501

echo ✅ 925stackai is up and running.
