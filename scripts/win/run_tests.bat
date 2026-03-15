@echo off
set "PYTEST_ADDOPTS=--reruns 1 --reruns-delay 2"
pipenv run pytest tests -v -l -s --brows chrome --url https://qa-reporting.pk1cloud.com/
exit /b %ERRORLEVEL%
