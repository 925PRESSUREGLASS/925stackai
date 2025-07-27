
@echo off
REM start_all.bat - launch GUI and API with optional port args
set GUI_PORT=%1
if "%GUI_PORT%"=="" set GUI_PORT=8501
set API_PORT=%2
if "%API_PORT%"=="" set API_PORT=8000

REM Activate virtual environment
call .venv\Scripts\activate.bat

REM Print Python version and environment info
python --version
where python
pip --version
pip list

REM Start Streamlit app
start cmd /k "streamlit run gui/app.py --server.port %GUI_PORT%"

REM Start FastAPI backend
start cmd /k "uvicorn app_quote_api:app --port %API_PORT% --reload"
