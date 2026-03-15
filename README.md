# SRM — Statistical Report Manager  
## Test Automation Framework  
**Stack:** Playwright · Python 3.11 · Pytest · Allure  
**App:** https://qa-reporting.pk1cloud.com/

---

## First-Time Setup on Your Laptop

### Step 1 — Install Python 3.11
Download from https://python.org → install → tick "Add to PATH"

### Step 2 — Open project in PyCharm
File → Open → select this `SRM/` folder → Open as Project  
PyCharm will detect no interpreter → Add Interpreter → Pipenv → OK

### Step 3 — Run setup script
Double-click `SETUP.bat`  
*(installs pipenv, all packages, and Playwright browsers)*

### Step 4 — Set your credentials
In PyCharm terminal:
```
set SRM_USER=your_email@example.com
set SRM_PASSWORD=your_password
```
Or: Run → Edit Configurations → Environment Variables → add both

---

## Running Tests

```bash
# All tests
scripts\win\run_tests.bat

# Specific file
pipenv run pytest tests/Account.py -v -s --brows chrome --url https://qa-reporting.pk1cloud.com/

# Specific test
pipenv run pytest tests/Account.py::test_verify_account_contains_all_sub_menus_T001 -v -s --brows chrome --url https://qa-reporting.pk1cloud.com/

# Headless (no browser window)
pipenv run pytest tests -v -s --brows chrome --headless --url https://qa-reporting.pk1cloud.com/

# Generate Allure report
pipenv run pytest tests -v -s --brows chrome --url https://qa-reporting.pk1cloud.com/ --alluredir=allure-results
allure serve allure-results
```

---

## Project Structure

```
SRM/
├── SETUP.bat                   ← Run this FIRST on a new laptop
├── conftest.py                 ← browser_page + frontend + log fixtures
├── pytest.ini                  ← Pytest settings
├── Pipfile                     ← All dependencies
├── pin_pipfile.py              ← Lock exact versions
│
├── scripts/win/
│   ├── run_tests.bat           ← Run all tests
│   ├── install_deps.bat        ← Install dependencies
│   └── codestyle.bat           ← Format + lint code
│
├── src/
│   ├── config/
│   │   ├── application.py      ← Frontend class (bundles all pages)
│   │   ├── credentials.py      ← AWS Secrets Manager
│   │   ├── env.py              ← URL, paths, credentials
│   │   └── logger.py           ← CustomLogger + Allure integration
│   │
│   ├── pages/
│   │   ├── login.py            ← LoginPage
│   │   ├── common.py           ← CommonElementsPage (sidebar, nav)
│   │   ├── home.py             ← HomeElementsPage (dashboard)
│   │   └── account.py          ← AccountElementsPage
│   │
│   └── utils/
│       ├── helper.py           ← UIHelper (table asserts, scroll)
│       └── test_data.py        ← Random data generators
│
├── tests/
│   ├── Account.py              ← T001–T009
│   ├── Account1.py             ← T010–T017
│   └── Addaccount.py           ← T018–T029
│
└── allure-results/             ← Auto-generated after test run
```

---

## Fixtures (conftest.py)

| Fixture | What you get |
|---|---|
| `browser_page` | Playwright Page — assign to `page = browser_page` |
| `frontend` | Frontend object: `.auth` `.home` `.common` `.account` `.helper` |
| `log` | Logger — `log.info("step done")` |

---

## CLI Options

| Flag | Default | Description |
|---|---|---|
| `--brows` | `chrome` | chrome, msedge, firefox, chromium, webkit |
| `--headless` | off | No browser window |
| `--url` | env.URL | Override app URL |
| `--brows-matrix` | None | Cross-browser CSV e.g. `chrome,firefox` |

---

## Push to Bitbucket

```bash
git init
git add .
git commit -m "Initial SRM automation framework"
git remote add origin https://bitbucket.org/perrknight/statreporterautomation.git
git push -u origin QA
```
