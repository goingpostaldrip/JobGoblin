@echo off
SETLOCAL ENABLEDELAYEDEXPANSION

TITLE JOB SCRAPER ULTIMATE
ECHO =============================================
ECHO            JOB SCRAPER ULTIMATE
ECHO Broad search engine discovery of job leads
ECHO =============================================

REM Prompt for keywords and locations
SET /p KEYWORDS=Enter keyword phrases (comma separated): 
SET /p LOCS=Enter location phrases (comma separated, blank for none): 
SET /p ENGINES=Enter engines (duckduckgo,simplyhired) or API (google_cse,bing,serpapi,linkedin,glassdoor) [default duckduckgo,simplyhired]: 
SET /p MAX=Max results per query (default 20): 
IF "%MAX%"=="" SET MAX=20

REM Default engines if none provided - free ones only
IF "%ENGINES%"=="" SET ENGINES=duckduckgo,simplyhired

SET OUTJSON=web_jobs_ultimate.json
SET OUTTXT=output\web_jobs_ultimate.txt
SET /p CSV=CSV output path (blank to skip): 
SET /p EXTRACT_EMAILS=Extract contact emails from found job postings? (Y/N, default N): 
IF /I "%EXTRACT_EMAILS%"=="" SET EXTRACT_EMAILS=N
IF /I "%EXTRACT_EMAILS%"=="y" SET EXTRACT_EMAILS=true
IF /I "%EXTRACT_EMAILS%"=="Y" SET EXTRACT_EMAILS=true

SET EMAILS_CSV=output\found_emails.csv
IF /I "%EXTRACT_EMAILS%"=="true" (
  ECHO Extracted emails will be saved to: %EMAILS_CSV%
  SET /p SEND_EMAILS=Send emails to extracted contacts? (Y/N, max 50/day, default N): 
  IF /I "%SEND_EMAILS%"=="" SET SEND_EMAILS=N
  IF /I "%SEND_EMAILS%"=="y" SET SEND_EMAILS=true
  IF /I "%SEND_EMAILS%"=="Y" SET SEND_EMAILS=true
) ELSE (
  SET SEND_EMAILS=N
)

SET /p EMAILTO=Email results to (comma separated, blank to skip): 
SET /p EMAILTOP=Email top N (default 10): 
IF "%EMAILTOP%"=="" SET EMAILTOP=10

ECHO.
ECHO =============================================
ECHO Running scrape with:
ECHO   Keywords: %KEYWORDS%
ECHO   Locations: %LOCS%
ECHO   Engines: %ENGINES%
ECHO   Max/query: %MAX%
ECHO =============================================
ECHO Output JSON: %OUTJSON%
ECHO Summary TXT: %OUTTXT%
IF NOT "%CSV%"=="" ECHO CSV: %CSV%
IF "%EXTRACT_EMAILS%"=="true" ECHO Extract Emails: YES
IF "%SEND_EMAILS%"=="true" ECHO Send Emails: YES (max 50/day)
IF NOT "%EMAILTO%"=="" ECHO Email to: %EMAILTO% (top %EMAILTOP%)
ECHO.

IF NOT EXIST output (mkdir output)

REM Build the CLI command based on options
SET CLI_CMD=python "%~dp0cli.py" --keywords "%KEYWORDS%" --locations "%LOCS%" --engines %ENGINES% --max-per-query %MAX% --out "%OUTJSON%" --txt-out "%OUTTXT%" --verbose

IF NOT "%CSV%"=="" (
  SET CLI_CMD=!CLI_CMD! --csv-out "%CSV%"
)

IF "%EXTRACT_EMAILS%"=="true" (
  SET CLI_CMD=!CLI_CMD! --extract-emails --emails-csv "%EMAILS_CSV%"
)

IF "%SEND_EMAILS%"=="true" (
  SET CLI_CMD=!CLI_CMD! --send-emails
)

IF NOT "%EMAILTO%"=="" (
  SET CLI_CMD=!CLI_CMD! --email-to "%EMAILTO%" --email-top %EMAILTOP%
)

ECHO Executing: %CLI_CMD%
ECHO.
%CLI_CMD%

IF ERRORLEVEL 1 (
  ECHO Scrape failed.
  EXIT /b 1
)

ECHO.
ECHO =============================================
ECHO Scrape complete!
ECHO =============================================
IF EXIST "%OUTTXT%" ECHO Summary: %OUTTXT%
IF "%EXTRACT_EMAILS%"=="true" ECHO Emails CSV: %EMAILS_CSV%
IF "%SEND_EMAILS%"=="true" ECHO Check output for email sending statistics
ECHO.
ECHO Press any key to exit...
PAUSE
FOR /F %%C IN ('python -c "import json;import sys;print(len(json.load(open(\"%OUTJSON%\", encoding=\"utf-8\"))))"') DO SET COUNTJSON=%%C
ECHO Total JSON records: %COUNTJSON%
IF "%COUNTJSON%"=="0" ECHO (No results - ensure engines include serpapi and API keys are set.)
ECHO First 10 lines:
SET COUNT=0
FOR /F "usebackq tokens=*" %%L IN ("%OUTTXT%") DO (
  SET /A COUNT+=1
  IF !COUNT! LEQ 10 ECHO %%L
)

ECHO.
ECHO You can re-run this batch file to perform another search.
ENDLOCAL
