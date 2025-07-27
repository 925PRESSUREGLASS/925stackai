@echo off
REM run_all.bat - Unified Windows launcher (merged)

REM 1. Python env & deps
if not exist .venv (
    python -m venv .venv
)
call .venv\Scripts\activate.bat
python --version
pip --version
pip install --upgrade pip >nul
pip install -r requirements.txt >nul

REM 2. (Optional) Rebuild vector index
REM python scripts\rebuild_index.py --input docs --store memory\vector_store

REM 3. (Optional) Docker Compose stack
REM docker compose --env-file .env up --build -d

REM 4. (Optional) Run tests
REM pytest -q

REM 5. Start Streamlit app in background
start "Streamlit" cmd /k streamlit run gui/app.py

REM 6. Start FastAPI app in background
start "FastAPI" cmd /k uvicorn app_quote_api:app --reload --port 8000

echo ✅ 925stackai is up and running. Open http://localhost:8501 for Streamlit and http://localhost:8000/docs for API docs.
pause
