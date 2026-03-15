import random
import string
from datetime import date, datetime, timedelta
from pathlib import Path

from dateutil.relativedelta import relativedelta

from src.config import env

# ── Paths ─────────────────────────────────────────────────────────────────────
downloads  = Path(env.ROOT) / "downloads-folder"
test_files = Path(env.ROOT) / "src" / "test_files"

# ── Timestamps & generated names ──────────────────────────────────────────────
timestamp    = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
current_time = datetime.now().strftime("%H:%M:%S")

project_name  = f"Test_Project_{timestamp}"
project_number = f"Number_{current_time}"
scope_title   = f"Scope_Title_{timestamp}"
description   = f"Test_Description_{timestamp}"
form          = f"Form_Name_{timestamp}"

# ── Dates ─────────────────────────────────────────────────────────────────────
dt_now  = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
today   = date.today().strftime("%m/%d/%Y")
today_1 = date.today().strftime("%m/%Y")

# ── Pre-generated random values ────────────────────────────────────────────────
rand_number_3   = random.getrandbits(10)
rand_number_5   = random.getrandbits(16)
rand_number_12  = random.getrandbits(40)
rand_number_100 = random.randint(1, 100)


# ── Helper functions ───────────────────────────────────────────────────────────

def future_date(days: int) -> str:
    """Return a date `days` from today as MM/DD/YYYY."""
    return (date.today() + timedelta(days=days)).strftime("%m/%d/%Y")


def random_future_date() -> str:
    """Return a random date within the next 365 days."""
    return (
        date.today() + relativedelta(days=random.randint(1, 365))
    ).strftime("%m/%d/%Y")


def past_date(days: int) -> str:
    """Return a date `days` before today as MM/DD/YYYY."""
    return (date.today() - timedelta(days=days)).strftime("%m/%d/%Y")


def day_of_current_month(day: int) -> str:
    """Return the given day of the current month as MM/DD/YYYY."""
    today_obj    = date.today()
    specific_day = today_obj.replace(day=day)
    return specific_day.strftime("%m/%d/%Y")


def random_past_date() -> str:
    """Return a random date within the last 365 days."""
    return (
        date.today() - relativedelta(days=random.randint(1, 365))
    ).strftime("%m/%d/%Y")


def random_digits(length: int) -> str:
    """Return a string of `length` random digits. e.g. random_digits(5) -> '84729'"""
    return "".join(str(random.randint(0, 9)) for _ in range(length))


def random_string(length: int) -> str:
    """Return `length` random uppercase letters + digits."""
    return "".join(random.choices(string.ascii_uppercase + string.digits, k=length))


def random_str(length: int) -> str:
    """Return `length` random uppercase letters only."""
    return "".join(random.choices(string.ascii_uppercase, k=length))


def random_number(min_val: int, max_val: int) -> int:
    """Return a random integer between min_val and max_val (inclusive)."""
    return random.randint(min_val, max_val)


def unique_name(suffix: str = "") -> str:
    """Return a unique numeric string. e.g. '156834'"""
    return f"{random.randrange(100000)}{suffix}"


def extract_digits(value: str) -> str:
    """Strip all non-digit characters from a string."""
    return "".join(filter(str.isdigit, value))


def any_rand_number(bits: int) -> str:
    return str(random.getrandbits(bits))


def random_non_numeric(
    length: int = 12,
    include_punct: bool = True,
    include_space: bool = False,
    include_unicode: bool = False,
) -> str:
    """Return a random string with no digits (0-9)."""
    pool = string.ascii_letters
    if include_punct:
        pool += '!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~'
    if include_space:
        pool += " "

    s = "".join(random.choice(pool) for _ in range(length))

    if include_unicode:
        extras = "😀🌍✨Привет世界"
        s = list(s)
        for i in range(min(3, len(s))):
            s[random.randrange(len(s))] = random.choice(extras)
        s = "".join(s)

    return s
