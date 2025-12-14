@echo off
REM Quick start for Windows users
REM This script sets up the environment and shows examples

SETLOCAL ENABLEDELAYEDEXPANSION
TITLE Job Scraper Ultimate - Quick Start

ECHO =========================================
ECHO  Job Scraper Ultimate - Quick Start
ECHO =========================================
ECHO.

REM Check if venv exists
IF NOT EXIST ".venv" (
    ECHO Creating virtual environment...
    python -m venv .venv
    IF ERRORLEVEL 1 (
        ECHO Error: Python not found. Please install Python 3.8 or later.
        PAUSE
        EXIT /b 1
    )
)

ECHO Activating virtual environment...
CALL .venv\Scripts\activate.bat

ECHO Installing requirements...
python -m pip install -r requirements.txt > nul 2>&1

REM Create output directory
IF NOT EXIST output (
    MKDIR output
)

ECHO.
ECHO =========================================
ECHO  Setup Complete!
ECHO =========================================
ECHO.
ECHO You can now run:
ECHO.
ECHO 1. Interactive Mode (Recommended):
ECHO    run_job_scraper.bat
ECHO.
ECHO 2. Command Line Examples:
ECHO.
ECHO    Basic scrape (no email extraction):
ECHO    python cli.py --keywords "Python Developer" --locations "New York" --engines duckduckgo,indeed
ECHO.
ECHO    Scrape + Extract Emails:
ECHO    python cli.py --keywords "Python Developer" --locations "New York" --engines duckduckgo,indeed --extract-emails
ECHO.
ECHO    Scrape + Extract + Send Emails (max 50/day):
ECHO    python cli.py --keywords "Python Developer" --locations "New York" --engines duckduckgo,indeed --extract-emails --send-emails
ECHO.
ECHO =========================================
ECHO  Email Configuration
ECHO =========================================
ECHO.
ECHO To enable email sending, set up environment variables:
ECHO.
ECHO Option 1: SendGrid (Free: 100 emails/day)
ECHO   set SENDGRID_API_KEY=SG.xxxxxxxxxxxxx
ECHO   set SMTP_USER=noreply@yourdomain.com
ECHO.
ECHO Option 2: Gmail SMTP
ECHO   set SMTP_HOST=smtp.gmail.com
ECHO   set SMTP_PORT=587
ECHO   set SMTP_USER=your@gmail.com
ECHO   set SMTP_PASSWORD=app_password
ECHO.
ECHO See .env.example for more options.
ECHO.
ECHO =========================================
ECHO Output files saved to:
ECHO   output\web_jobs_ultimate.json (all jobs)
ECHO   output\web_jobs_ultimate.txt (summary)
ECHO   output\found_emails.csv (extracted emails)
ECHO =========================================
ECHO.
PAUSE
