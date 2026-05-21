@echo off
title SecureScan GUI
echo ========================================
echo    SecureScan GUI Launcher
echo    FOR EDUCATIONAL PURPOSES ONLY
echo ========================================
echo.

REM Check if virtual environment exists
if exist venv\ (
    echo Activating virtual environment...
    call venv\Scripts\activate
)

REM Install requirements if needed
pip show requests > nul 2>&1
if errorlevel 1 (
    echo Installing requirements...
    pip install requests
)

echo.
echo Starting GUI...
python run_gui.py

pause