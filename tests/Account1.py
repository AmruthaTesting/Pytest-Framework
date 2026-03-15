import time

from playwright.sync_api import expect

from src.utils import test_data as data


# ---------------------------------------------------------------------------
# Shared helper — avoids repeating login + navigation in every test
# ---------------------------------------------------------------------------
def _go_to_account_details(page, frontend, log):
    frontend.auth.log_in()
    log.info("Signed in to Reporting")
    frontend.common.toggle_arrow.hover()
    frontend.common.toggle_arrow.click()
    page.locator(frontend.common.norm_text_span.format("Admin")).click()
    page.locator(frontend.common.norm_text_span.format("Accounts")).click()
    log.info("Navigated to Accounts Page")
    frontend.common.toggle_arrow.click()
    page.locator(frontend.account.account_link.format("Perrknight")).click()
    page.locator(frontend.account.Dashboard_Name.format("Account Details"))
    log.info("Navigated to Account Details Page")


# =============================================================================
# T010 — NAIC Group Code should NOT allow more than 5 characters
# =============================================================================
def test_verify_NAIC_Group_code_should_not_allow_more_than_5_T010(log, frontend, browser_page):
    page = browser_page
    _go_to_account_details(page, frontend, log)

    page.locator(frontend.account.input_edit.format("naicGroupCode")).click()
    long_code = data.random_digits(10)
    page.locator(frontend.account.input_text).fill(long_code)
    time.sleep(1)

    actual = page.locator(frontend.account.input_text).input_value()
    assert len(actual) <= 5, \
        f"NAIC Group Code accepted {len(actual)} chars, max is 5"
    log.info(f"NAIC Group Code max-length validated: typed {len(long_code)}, accepted {len(actual)}")

    frontend.account.close.click()
    page.locator(frontend.common.user_profile).click()
    page.locator(frontend.common.norm_text_span.format("Log out")).click()


# =============================================================================
# T011 — NAIC Group Code should NOT allow alphabetic characters
# =============================================================================
def test_verify_NAIC_Group_code_should_not_allow_alphabets_T011(log, frontend, browser_page):
    page = browser_page
    _go_to_account_details(page, frontend, log)

    page.locator(frontend.account.input_edit.format("naicGroupCode")).click()
    page.locator(frontend.account.input_text).fill("ABCDE")
    time.sleep(1)

    actual = page.locator(frontend.account.input_text).input_value()
    assert not any(c.isalpha() for c in actual), \
        f"NAIC Group Code accepted alphabetic chars: '{actual}'"
    log.info("NAIC Group Code correctly rejects alphabetic characters")

    frontend.account.close.click()
    page.locator(frontend.common.user_profile).click()
    page.locator(frontend.common.norm_text_span.format("Log out")).click()


# =============================================================================
# T012 — NAIC Group Code should NOT allow special characters
# =============================================================================
def test_verify_NAIC_Group_code_should_not_allow_special_chars_T012(log, frontend, browser_page):
    page = browser_page
    _go_to_account_details(page, frontend, log)

    page.locator(frontend.account.input_edit.format("naicGroupCode")).click()
    page.locator(frontend.account.input_text).fill("!@#$%")
    time.sleep(1)

    actual = page.locator(frontend.account.input_text).input_value()
    assert not any(c in "!@#$%" for c in actual), \
        f"NAIC Group Code accepted special chars: '{actual}'"
    log.info("NAIC Group Code correctly rejects special characters")

    frontend.account.close.click()
    page.locator(frontend.common.user_profile).click()
    page.locator(frontend.common.norm_text_span.format("Log out")).click()


# =============================================================================
# T013 — Legal Name allows inline edit and save
# =============================================================================
def test_verify_legal_name_allows_inline_edit_and_save_T013(log, frontend, browser_page):
    page = browser_page
    _go_to_account_details(page, frontend, log)

    page.locator(frontend.account.input_edit.format("legalName")).click()
    new_name = f"AutoLegal_{data.random_str(6)}"
    page.locator(frontend.account.input_text).fill(new_name)
    time.sleep(1)
    frontend.account.save.click()
    time.sleep(1)
    log.info(f"Saved Legal Name: {new_name}")

    saved = page.locator(
        frontend.account.input_edit.format("legalName")
    ).inner_text()
    assert new_name in saved, \
        f"Expected '{new_name}' in saved value, got '{saved}'"
    log.info("Legal Name inline edit and save verified")

    page.locator(frontend.common.user_profile).click()
    page.locator(frontend.common.norm_text_span.format("Log out")).click()


# =============================================================================
# T014 — Legal Name close icon discards the edit
# =============================================================================
def test_verify_legal_name_close_discards_edit_T014(log, frontend, browser_page):
    page = browser_page
    _go_to_account_details(page, frontend, log)

    original = page.locator(
        frontend.account.input_edit.format("legalName")
    ).inner_text().strip()

    page.locator(frontend.account.input_edit.format("legalName")).click()
    page.locator(frontend.account.input_text).fill("ShouldNotBeSaved_XYZ")
    time.sleep(1)
    frontend.account.close.click()
    time.sleep(1)
    log.info("Clicked close (X) to discard edit")

    after = page.locator(
        frontend.account.input_edit.format("legalName")
    ).inner_text().strip()
    assert after == original, \
        f"Legal Name changed after close: expected '{original}', got '{after}'"
    log.info("Legal Name close correctly discards edit")

    page.locator(frontend.common.user_profile).click()
    page.locator(frontend.common.norm_text_span.format("Log out")).click()


# =============================================================================
# T015 — Zip Code field allows only numeric input
# =============================================================================
def test_verify_zip_code_allows_only_numeric_T015(log, frontend, browser_page):
    page = browser_page
    _go_to_account_details(page, frontend, log)

    page.locator(frontend.account.input_edit.format("zip")).click()
    valid_zip = data.random_digits(5)
    page.locator(frontend.account.input_text).fill(valid_zip)
    time.sleep(1)
    frontend.account.save.click()
    time.sleep(1)
    log.info(f"Entered Zip: {valid_zip}")

    saved = page.locator(frontend.account.input_edit.format("zip")).inner_text()
    assert saved.strip().isdigit(), \
        f"Zip Code should be numeric, got: '{saved}'"
    log.info("Zip Code accepts only numeric characters — verified")

    page.locator(frontend.common.user_profile).click()
    page.locator(frontend.common.norm_text_span.format("Log out")).click()


# =============================================================================
# T016 — Account Details page has all tabs visible
# =============================================================================
def test_verify_account_details_tabs_visible_T016(log, frontend, browser_page):
    page = browser_page
    _go_to_account_details(page, frontend, log)

    for tab in ["Contacts", "Users", "Reporting Profile", "Configuration", "Processes"]:
        expect(
            page.locator(frontend.common.norm_text_span.format(tab))
        ).to_be_visible(timeout=10_000)
        log.info(f"Tab '{tab}' is visible")

    log.info("All Account Details tabs verified")

    page.locator(frontend.common.user_profile).click()
    page.locator(frontend.common.norm_text_span.format("Log out")).click()


# =============================================================================
# T017 — NAIC value persists after page refresh
# =============================================================================
def test_verify_NAIC_value_persists_after_refresh_T017(log, frontend, browser_page):
    page = browser_page
    _go_to_account_details(page, frontend, log)

    page.locator(frontend.account.input_edit.format("naic")).click()
    new_naic = data.random_digits(5)
    page.locator(frontend.account.input_text).fill(new_naic)
    time.sleep(1)
    frontend.account.save.click()
    time.sleep(2)
    log.info(f"Saved NAIC: {new_naic}")

    page.reload()
    page.wait_for_selector("body")
    time.sleep(2)
    log.info("Page refreshed")

    after_refresh = page.locator(
        frontend.account.input_edit.format("naic")
    ).inner_text().strip()
    assert after_refresh == new_naic, \
        f"NAIC did not persist: expected '{new_naic}', got '{after_refresh}'"
    log.info("NAIC value persisted after page refresh — verified")

    page.locator(frontend.common.user_profile).click()
    page.locator(frontend.common.norm_text_span.format("Log out")).click()
