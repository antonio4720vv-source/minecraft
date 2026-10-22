@echo off
cd /d "%~dp0"
if not exist .venv (
  echo Instalando JARVIS por primera vez...
  python -m venv .venv
  .venv\Scripts\python -m pip install -r requirements.txt
)
if not exist .env (
  copy .env.example .env >nul
  echo Completa GEMINI_API_KEY en el archivo .env y volve a abrir esto.
  notepad .env
  pause
  exit /b
)
.venv\Scripts\python jarvis.py %*
pause
