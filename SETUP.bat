@echo off
echo ============================================================
echo   SRM Automation Framework - First Time Setup
echo ============================================================
echo.

REM Step 1 - Check Python
echo [1/5] Checking Python installation...
python --version >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo ERROR: Python not found. Install Python 3.11 from python.org first.
    pause
    exit /b 1
)
python --version
echo Python found OK.
echo.

REM Step 2 - Install pipenv
echo [2/5] Installing pipenv...
pip install pipenv
echo.

REM Step 3 - Set encoding
SET LANG=en_US.UTF-8
SET LC_ALL=en_US.UTF-8

REM Step 4 - Install all project dependencies
echo [3/5] Installing project dependencies from Pipfile...
pipenv install --ignore-pipfile
echo.

REM Step 5 - Install Playwright browsers
echo [4/5] Installing Playwright browsers (Chrome/Firefox)...
pipenv run playwright install
echo.

REM Step 6 - Verify
echo [5/5] Verifying setup...
pipenv run python -c "import playwright; print('Playwright OK')"
pipenv run python -c "import pytest; print('Pytest OK')"
pipenv run python -c "import allure; print('Allure OK')"
echo.

echo ============================================================
echo   Setup Complete! 
echo   Now set your credentials:
echo     SRM_USER     = your login email
echo     SRM_PASSWORD = your password
echo.
echo   Then run:  scripts\win\run_tests.bat
echo ============================================================
pause
