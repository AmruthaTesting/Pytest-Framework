@echo off
REM Format code using Black (default line length is already 88)
python -m pipenv run black ./src ./tests

REM Check code style with pycodestyle (explicitly set max line length)
python -m pipenv run pycodestyle --max-line-length=88 ./src ./tests
