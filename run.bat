@echo off
REM JobGoblin - Lead Finder Launch Script for Windows
REM Created by NERDY BIRD IT

setlocal enabledelayedexpansion

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo.
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.7+ from https://www.python.org/
    echo Make sure to check "Add Python to PATH" during installation
    echo.
    pause
    exit /b 1
)

REM Check if venv exists, if not create it
if not exist "venv\" (
    echo.
    echo Creating virtual environment...
    echo.
    python -m venv venv
)

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Check if requirements are installed
pip show ttkbootstrap >nul 2>&1
if %errorlevel% neq 0 (
    echo.
    echo Installing dependencies...
    echo.
    pip install -r requirements.txt
)

REM Run the GUI
echo.
echo Starting JobGoblin - Lead Finder...
echo.
python gui_app.py

REM If GUI exits, pause so user can see any error messages
pause
