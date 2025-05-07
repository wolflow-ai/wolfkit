REM This commented out version allows one to run a command line behind the app, if required.
REM otherwise, use the non-commented out version.

REM @echo off
REM cd /d %~dp0
REM call venv\Scripts\activate.bat
REM python main.py
REM pause

@echo off
cd /d %~dp0
call venv\Scripts\activate.bat
start "" pythonw main.py > log.txt 2>&1

