import os
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Credentials
# ---------------------------------------------------------------------------
# Option 1 — AWS Secrets Manager (used in CI / production)
# Option 2 — Environment variables (used for local development)
#
# To run locally, set these two variables on your Windows laptop:
#   Method A (Command Prompt):
#       set SRM_USER=your_email@example.com
#       set SRM_PASSWORD=your_password
#
#   Method B (PyCharm Run Config):
#       Run -> Edit Configurations -> Environment Variables
#       Add:  SRM_USER = your_email@example.com
#             SRM_PASSWORD = your_password
#
#   Method C (System Environment Variables - permanent):
#       Windows Search -> "Edit the system environment variables"
#       -> Environment Variables -> New
# ---------------------------------------------------------------------------
try:
    from src.config import credentials as cred
    USER = cred.USER()
    PASSWORD = cred.PASSWORD()
except Exception:
    USER = os.getenv("SRM_USER", "")
    PASSWORD = os.getenv("SRM_PASSWORD", "")

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
ROOT = Path(__file__).resolve().parents[2]
CACHE_FOLDER = ROOT / ".pytest_cache"
DOWNLOADS_DIR = ROOT / "downloads-folder"

# ---------------------------------------------------------------------------
# App settings
# ---------------------------------------------------------------------------
RESOLUTION = os.getenv("RESOLUTION", "1460")
URL = os.getenv("URL", "https://qa-reporting.pk1cloud.com/")
ONE_SESSION = True
IS_PARALLEL = "-n" in " ".join(sys.argv)
