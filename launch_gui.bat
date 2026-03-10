@echo off
REM Launch Job Scraper Ultimate GUI

TITLE Job Scraper Ultimate - GUI Launcher

ECHO =========================================
ECHO  Job Scraper Ultimate - GUI Edition
ECHO =========================================
ECHO.

REM Check if venv exists
IF NOT EXIST ".venv" (
    ECHO Setting up for first time...
    ECHO Creating virtual environment...
    python -m venv .venv
    IF ERRORLEVEL 1 (
        ECHO Error: Python not found. Please install Python 3.8 or later.
        PAUSE
        EXIT /b 1
    )
    
    ECHO Installing requirements...
    CALL .venv\Scripts\activate.bat
    python -m pip install --upgrade pip
    python -m pip install -r requirements.txt
) ELSE (
    CALL .venv\Scripts\activate.bat
)

REM Create output directory
IF NOT EXIST output (
    MKDIR output
)

ECHO Launching GUI...
ECHO.

python gui_app.py

IF ERRORLEVEL 1 (
    ECHO.
    ECHO Error launching GUI. Make sure all requirements are installed.
    ECHO Try running: pip install -r requirements.txt
    PAUSE
)
