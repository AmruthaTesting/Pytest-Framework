import os
import shutil
import subprocess
import threading

import allure
import pytest
from playwright.sync_api import sync_playwright

from src.config.application import Frontend
from src.config import env
from src.config.logger import setup_logging

logger = setup_logging()

# =============================================================================
# PYTEST CONFIG HOOKS
# =============================================================================

def pytest_configure(config):
    logger.info("Start pytest configuring")
    if os.getenv("GENERATE_REPORT", "True").lower() in ("true", "1", "yes"):
        reports_dir = "allure-results"
        logger.info(f"Deleting report dir: {reports_dir}")
        try:
            shutil.rmtree(reports_dir)
        except FileNotFoundError:
            pass
        os.makedirs(reports_dir, exist_ok=True)
        logger.info("Created fresh report dir")


def pytest_unconfigure():
    if os.getenv("GENERATE_REPORT", "True").lower() in ("true", "1", "yes"):
        logger.info("### Create allure report")
        try:
            subprocess.check_call(
                args="allure generate -c allure-results", shell=True
            )
        except subprocess.CalledProcessError:
            logger.warning(
                "!!! Allure: cannot create report - report dir is empty"
            )


# =============================================================================
# BROWSER OPTIONS
# =============================================================================

CHANNELS = {
    "chrome", "chrome-beta", "chrome-dev", "chrome-canary",
    "msedge", "msedge-beta", "msedge-dev", "msedge-canary",
}
ENGINES = {"chromium", "firefox", "webkit"}


def pytest_addoption(parser):
    parser.addoption(
        "--brows", default="chrome",
        help="chrome|msedge|firefox|chromium|webkit (default: chrome)",
    )
    parser.addoption(
        "--brows-matrix", default=None,
        help="CSV list for parallel cross-browser: e.g. 'chrome,msedge,firefox'",
    )
    parser.addoption(
        "--headless", action="store_true",
        help="Run in headless mode (default: headed)",
    )
    parser.addoption(
        "--url", default=None,
        help="Override the start URL",
    )
    parser.addoption(
        "--channel", default=None,
        help="Force a specific Chromium channel",
    )
    parser.addoption(
        "--executable-path", default=None,
        help="Full path to a custom browser binary",
    )
    parser.addoption(
        "--user-data-dir", default=None,
        help="Persistent profile directory",
    )
    parser.addoption(
        "--cdp", default=None,
        help="Connect via CDP e.g. http://localhost:9222",
    )


def pytest_generate_tests(metafunc):
    if "brows" in metafunc.fixturenames:
        matrix = metafunc.config.getoption("--brows-matrix")
        if matrix:
            items = [b.strip() for b in matrix.split(",") if b.strip()]
            assert items, "Empty --brows-matrix"
            metafunc.parametrize("brows", items, indirect=True)


@pytest.fixture(scope="function")
def brows(request):
    return getattr(request, "param", None) or request.config.getoption("--brows")


@pytest.fixture(scope="function")
def headless(request):
    return bool(request.config.getoption("--headless"))


@pytest.fixture(scope="function")
def url(request):
    return request.config.getoption("--url")


# =============================================================================
# ZOOM HELPERS  (keeps layout consistent across browsers)
# =============================================================================

def _apply_cross_browser_zoom(page, engine_or_channel: str, scale: float = 0.5):
    b = (engine_or_channel or "").lower()
    if b in CHANNELS | {"chromium", "chrome", "msedge"}:
        page.evaluate(f"document.documentElement.style.zoom='{scale}'")
        return
    if b == "firefox":
        page.add_style_tag(
            content=f"html {{ transform: scale({scale}); transform-origin: 0 0; }}"
        )
        return
    # WebKit fallback
    page.evaluate(f"document.documentElement.style.zoom='{scale}'")


def _install_zoom_init_script(context, engine_or_channel: str, scale: float = 0.5):
    b = (engine_or_channel or "").lower()
    if b in CHANNELS | {"chromium", "chrome", "msedge"}:
        context.add_init_script(f"""
            (() => {{
                const apply = () => {{
                    try {{ document.documentElement.style.zoom = "{scale}"; }} catch(e) {{}}
                }};
                apply();
                document.addEventListener("DOMContentLoaded", apply);
            }})();
        """)
        return
    if b == "firefox":
        context.add_init_script(f"""
            (() => {{
                const ID = "__pw_zoom_style__";
                const apply = () => {{
                    try {{
                        if (document.getElementById(ID)) return;
                        const style = document.createElement("style");
                        style.id = ID;
                        style.textContent = `html {{ transform: scale({scale}); transform-origin: 0 0; }}`;
                        (document.head || document.documentElement).appendChild(style);
                    }} catch(e) {{}}
                }};
                apply();
                document.addEventListener("DOMContentLoaded", apply);
            }})();
        """)
        return
    # WebKit fallback
    context.add_init_script(f"""
        (() => {{
            const apply = () => {{
                try {{ document.documentElement.style.zoom = "{scale}"; }} catch(e) {{}}
            }};
            apply();
            document.addEventListener("DOMContentLoaded", apply);
        }})();
    """)


# =============================================================================
# BROWSER FIXTURE
# =============================================================================

@pytest.fixture(scope="function")
def browser_page(brows, headless, url, request):
    """
    Launch a browser, apply 0.5x zoom, open the app URL.
    Yields a Playwright Page object to the test.
    Auto-captures a screenshot on teardown (last_screenshot.png).
    """
    with sync_playwright() as p:
        browser = None
        context = None

        channel_opt     = request.config.getoption("--channel") or None
        executable_path = request.config.getoption("--executable-path") or None
        user_data_dir   = request.config.getoption("--user-data-dir") or None
        cdp_url         = request.config.getoption("--cdp") or None

        launch_args      = ["--start-maximized"] if not headless else []
        headed_viewport  = None
        headless_viewport = {"width": 1920, "height": 1080}

        b = (brows or "chrome").strip().lower()

        # ── CDP attach ────────────────────────────────────────────────────────
        if cdp_url:
            if b in CHANNELS or b in {"chromium", "chrome", "msedge"}:
                context = p.chromium.connect_over_cdp(cdp_url).contexts[0]
            else:
                raise ValueError("--cdp is for Chromium-family browsers only")

        else:
            # ── Channel flag (highest priority) ───────────────────────────────
            if channel_opt:
                if b in {"firefox", "webkit"}:
                    raise ValueError("--channel is for Chromium-family browsers only")
                browser = p.chromium.launch(
                    channel=channel_opt, headless=headless,
                    args=launch_args, executable_path=executable_path,
                )
                context = browser.new_context(
                    accept_downloads=True,
                    viewport=headed_viewport if not headless else headless_viewport,
                )

            # ── Known channel  e.g. chrome / msedge ───────────────────────────
            elif b in CHANNELS or b in {"chrome", "msedge"}:
                browser = p.chromium.launch(
                    channel="msedge" if b == "edge" else b,
                    headless=headless, args=launch_args,
                    executable_path=executable_path,
                )
                context = browser.new_context(
                    accept_downloads=True,
                    viewport=headed_viewport if not headless else headless_viewport,
                )

            # ── Playwright built-in engines ────────────────────────────────────
            elif b == "chromium":
                browser = p.chromium.launch(
                    headless=headless, args=launch_args,
                    executable_path=executable_path,
                )
                context = browser.new_context(
                    accept_downloads=True,
                    viewport=headed_viewport if not headless else headless_viewport,
                )
            elif b == "firefox":
                browser = p.firefox.launch(headless=headless)
                context = browser.new_context(
                    accept_downloads=True,
                    viewport={"width": 1920, "height": 1080},
                    screen={"width": 1920, "height": 1080},
                )
            elif b == "webkit":
                browser = p.webkit.launch(headless=headless)
                context = browser.new_context(
                    accept_downloads=True,
                    viewport={"width": 1920, "height": 1080},
                    screen={"width": 1920, "height": 1080},
                )
            else:
                raise ValueError(f"Unsupported --brows='{brows}'")

        # ── Install zoom init script (persists across page navigations) ────────
        try:
            _install_zoom_init_script(context, b, scale=0.5)
        except Exception:
            pass

        page = context.new_page()
        page.set_default_timeout(10_000)

        if url:
            page.goto(url)
            page.wait_for_selector("body")

        # Apply zoom immediately after first load
        try:
            _apply_cross_browser_zoom(page, b, scale=0.5)
        except Exception:
            pass

        try:
            yield page
        finally:
            # Always save last screenshot
            try:
                page.screenshot(path="allure-results/last_screenshot.png")
            except Exception:
                pass
            # Clean shutdown
            try:
                context.close()
            finally:
                if browser and hasattr(browser, "close"):
                    try:
                        browser.close()
                    except Exception:
                        pass


# =============================================================================
# APPLICATION FIXTURE
# =============================================================================

@pytest.fixture(scope="function")
def frontend(browser_page):
    """Returns the Frontend facade — gives access to all page objects."""
    return Frontend(browser_page)


# =============================================================================
# SHARED FIXTURES
# =============================================================================

@pytest.fixture(scope="session")
def my_drive():
    return env.DOWNLOADS_DIR


@pytest.fixture(scope="session")
def log():
    return logger


# =============================================================================
# HOOKS — LOGGING & SCREENSHOT ON FAILURE
# =============================================================================

def pytest_runtest_setup(item):
    threading.current_thread().__name__ = item.name
    logger.test_log.truncate(0)
    logger.test_log.seek(0)
    logger.info("==== Run fixtures ====")


def pytest_runtest_call():
    logger.info("Run test step")


def pytest_runtest_teardown():
    logger.info("Stop test step")
    logger.info("==== Stop fixtures ====")


def pytest_runtest_makereport(item, call):
    if call.when == "call":
        # Attach logs to Allure report
        logger.attach_debug("logs", logger.test_log.getvalue())

        # Screenshot on failure
        if call.excinfo:
            page = item.funcargs.get("browser_page") or item.funcargs.get("page")
            if page:
                try:
                    screenshot_bytes = page.screenshot(full_page=True)
                    allure.attach(
                        screenshot_bytes,
                        name="Failure Screenshot",
                        attachment_type=allure.attachment_type.PNG,
                    )
                except Exception as e:
                    logger.warning(f"Couldn't capture screenshot: {e}")
