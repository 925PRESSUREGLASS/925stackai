
@echo off
REM Activate virtual environment
call .venv\Scripts\activate.bat

REM Print Python version and environment info
python --version
where python
pip --version
pip list

REM Start Streamlit app
start cmd /k "streamlit run gui/app.py"

REM Start FastAPI backend
start cmd /k "uvicorn app_quote_api:app --reload"
