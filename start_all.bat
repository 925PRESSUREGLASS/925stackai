@echo off
call .venv\Scripts\activate.bat
start cmd /k "streamlit run gui/app.py"
start cmd /k "uvicorn app_quote_api:app --reload"
