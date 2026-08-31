@echo off
REM runserver.bat — quick startup for development on Windows
REM Place this at the project root (where manage.py lives).

REM By default it looks for a virtualenv at .venv; change VENV_PATH if needed.
SET VENV_PATH=%~dp0.venv

IF EXIST "%VENV_PATH%\Scripts\activate.bat" (
  call "%VENV_PATH%\Scripts\activate.bat"
) ELSE (
  echo Virtualenv not found at %VENV_PATH%\nPlease activate your venv manually or edit this file to point to your Python.
)

REM Bind to 127.0.0.1 to avoid exposing the dev server publicly
python manage.py runserver 127.0.0.1:8000

pause
