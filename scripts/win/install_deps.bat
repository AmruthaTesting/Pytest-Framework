@echo off
REM Install pipenv if not already available
where pipenv >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo Installing pipenv...
    pip3 install pipenv
)

REM Set environment variables to prevent encoding issues
SET LANG=en_US.UTF-8
SET LC_ALL=en_US.UTF-8

REM Install project dependencies
pipenv install --ignore-pipfile

REM Install Playwright browsers
pipenv run playwright install
