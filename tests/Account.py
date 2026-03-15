import time

from playwright.sync_api import expect

from src.utils import test_data as data


# =============================================================================
# T001 — Sidebar contains all Admin sub-menus
# =============================================================================
def test_verify_account_contains_all_sub_menus_T001(log, frontend, browser_page):
    page = browser_page

    frontend.auth.log_in()
    log.info("Signed in to Reporting")

    expect(frontend.common.toggle_arrow).to_be_visible(timeout=10_000)
    frontend.common.toggle_arrow.hover()
    frontend.common.toggle_arrow.click()

    for menu in ["Admin", "Accounts", "Users", "Roles", "Settings"]:
        expect(
            page.locator(frontend.common.norm_text_span.format(menu))
        ).to_be_visible()
    log.info("All Admin sub-menus verified")

    page.locator(frontend.common.user_profile).click()
    page.locator(frontend.common.norm_text_span.format("Log out")).click()


# =============================================================================
# T002 — User can see Account Details page
# =============================================================================
def test_verify_user_able_to_see_account_details_page_T002(log, frontend, browser_page):
    page = browser_page

    frontend.auth.log_in()
    log.info("Signed in to Reporting")

    frontend.common.toggle_arrow.hover()
    frontend.common.toggle_arrow.click()
    page.locator(frontend.common.norm_text_span.format("Admin")).click()
    page.locator(frontend.common.norm_text_span.format("Accounts")).click()
    log.info("Navigated to Accounts Page")

    frontend.common.toggle_arrow.click()
    page.locator(frontend.account.account_link.format("Perrknight")).click()

    expect(
        page.locator(frontend.account.Dashboard_Name.format("Account Details"))
    ).to_be_visible(timeout=10_000)
    log.info("Navigated to Account Details Page")

    page.locator(frontend.common.norm_text_span.format("BACK")).click()
    log.info("Navigated to Default Page")

    page.locator(frontend.common.user_profile).click()
    page.locator(frontend.common.norm_text_span.format("Log out")).click()


# =============================================================================
# T003 — All required fields are visible on Account Details
# =============================================================================
def test_verify_all_necessary_fields_should_be_able_to_see_T003(log, frontend, browser_page):
    page = browser_page

    frontend.auth.log_in()
    log.info("Signed in to Reporting")

    frontend.common.toggle_arrow.hover()
    frontend.common.toggle_arrow.click()
    page.locator(frontend.common.norm_text_span.format("Admin")).click()
    page.locator(frontend.common.norm_text_span.format("Accounts")).click()
    log.info("Navigated to Accounts Page")

    frontend.common.toggle_arrow.click()
    page.locator(frontend.account.account_link.format("Perrknight")).click()
    log.info("Navigated to Account Details Page")

    for field in ["NAIC #:*", "NAIC Group Code:*", "Legal Name:*"]:
        expect(
            page.locator(frontend.account.field_name.format(field))
        ).to_be_visible()

    for label in ["Phone:*", "Zip Code:*"]:
        expect(
            page.locator(frontend.common.norm_text_span.format(label))
        ).to_be_visible()

    log.info("All required fields visible")

    page.locator(frontend.common.user_profile).click()
    page.locator(frontend.common.norm_text_span.format("Log out")).click()


# =============================================================================
# T004 — All necessary fields allow inline editing
# =============================================================================
def test_verify_all_necessary_fields_allow_inline_editing_account_T004(log, frontend, browser_page):
    page = browser_page

    frontend.auth.log_in()
    log.info("Signed in to Reporting")

    frontend.common.toggle_arrow.hover()
    frontend.common.toggle_arrow.click()
    page.locator(frontend.common.norm_text_span.format("Admin")).click()
    page.locator(frontend.common.norm_text_span.format("Accounts")).click()
    log.info("Navigated to Accounts Page")

    frontend.common.toggle_arrow.click()
    page.locator(frontend.account.account_link.format("Perrknight")).click()
    log.info("Navigated to Account Details Page")

    for field in ["naic", "legalName", "naicGroupCode", "zip"]:
        page.locator(frontend.account.input_edit.format(field)).click()
        frontend.account.close.click()
        time.sleep(1)
        log.info(f"{field} allowing to inline edit option")

    page.locator(frontend.common.user_profile).click()
    page.locator(frontend.common.norm_text_span.format("Log out")).click()


# =============================================================================
# T005 — NAIC Number allows only numeric characters
# =============================================================================
def test_verify_NAIC_Number_allow_only_Numeric_characters_T005(log, frontend, browser_page):
    page = browser_page

    frontend.auth.log_in()
    log.info("Signed in to Reporting")

    frontend.common.toggle_arrow.hover()
    frontend.common.toggle_arrow.click()
    page.locator(frontend.common.norm_text_span.format("Admin")).click()
    page.locator(frontend.common.norm_text_span.format("Accounts")).click()
    frontend.common.toggle_arrow.click()
    page.locator(frontend.account.account_link.format("Perrknight")).click()
    log.info("Navigated to Account Details Page")

    page.locator(frontend.account.input_edit.format("naic")).click()
    valid_naic = data.random_digits(5)
    page.locator(frontend.account.input_text).fill(valid_naic)
    time.sleep(1)
    frontend.account.save.click()
    log.info(f"Entered NAIC: {valid_naic}")

    saved = page.locator(frontend.account.input_edit.format("naic")).inner_text()
    assert saved.strip().isdigit(), f"NAIC should be numeric, got: {saved}"
    log.info("NAIC field accepts only numeric characters — verified")

    page.locator(frontend.common.user_profile).click()
    page.locator(frontend.common.norm_text_span.format("Log out")).click()


# =============================================================================
# T006 — NAIC Number should NOT allow more than 5 characters
# =============================================================================
def test_verify_NAIC_Number_should_not_allow_more_than_5_T006(log, frontend, browser_page):
    page = browser_page

    frontend.auth.log_in()
    log.info("Signed in to Reporting")

    frontend.common.toggle_arrow.hover()
    frontend.common.toggle_arrow.click()
    page.locator(frontend.common.norm_text_span.format("Admin")).click()
    page.locator(frontend.common.norm_text_span.format("Accounts")).click()
    frontend.common.toggle_arrow.click()
    page.locator(frontend.account.account_link.format("Perrknight")).click()
    log.info("Navigated to Account Details Page")

    page.locator(frontend.account.input_edit.format("naic")).click()
    long_naic = data.random_digits(10)
    page.locator(frontend.account.input_text).fill(long_naic)
    time.sleep(1)

    actual = page.locator(frontend.account.input_text).input_value()
    assert len(actual) <= 5, f"NAIC accepted {len(actual)} chars, max is 5"
    log.info(f"NAIC max-length validated: typed {len(long_naic)}, accepted {len(actual)}")

    frontend.account.close.click()
    page.locator(frontend.common.user_profile).click()
    page.locator(frontend.common.norm_text_span.format("Log out")).click()


# =============================================================================
# T007 — NAIC Number should NOT allow alphabetic characters
# =============================================================================
def test_verify_NAIC_Number_should_not_allow_characters_alpha_T007(log, frontend, browser_page):
    page = browser_page

    frontend.auth.log_in()
    log.info("Signed in to Reporting")

    frontend.common.toggle_arrow.hover()
    frontend.common.toggle_arrow.click()
    page.locator(frontend.common.norm_text_span.format("Admin")).click()
    page.locator(frontend.common.norm_text_span.format("Accounts")).click()
    frontend.common.toggle_arrow.click()
    page.locator(frontend.account.account_link.format("Perrknight")).click()
    log.info("Navigated to Account Details Page")

    page.locator(frontend.account.input_edit.format("naic")).click()
    page.locator(frontend.account.input_text).fill("ABCDE")
    time.sleep(1)

    actual = page.locator(frontend.account.input_text).input_value()
    assert not any(c.isalpha() for c in actual), \
        f"NAIC accepted alphabetic chars: '{actual}'"
    log.info("NAIC field correctly rejects alphabetic characters")

    frontend.account.close.click()
    page.locator(frontend.common.user_profile).click()
    page.locator(frontend.common.norm_text_span.format("Log out")).click()


# =============================================================================
# T008 — NAIC Number should NOT allow special characters
# =============================================================================
def test_verify_NAIC_Number_should_not_allow_characters_special_T008(log, frontend, browser_page):
    page = browser_page

    frontend.auth.log_in()
    log.info("Signed in to Reporting")

    frontend.common.toggle_arrow.hover()
    frontend.common.toggle_arrow.click()
    page.locator(frontend.common.norm_text_span.format("Admin")).click()
    page.locator(frontend.common.norm_text_span.format("Accounts")).click()
    frontend.common.toggle_arrow.click()
    page.locator(frontend.account.account_link.format("Perrknight")).click()
    log.info("Navigated to Account Details Page")

    page.locator(frontend.account.input_edit.format("naic")).click()
    page.locator(frontend.account.input_text).fill("!@#$%")
    time.sleep(1)

    actual = page.locator(frontend.account.input_text).input_value()
    assert not any(c in "!@#$%" for c in actual), \
        f"NAIC accepted special chars: '{actual}'"
    log.info("NAIC field correctly rejects special characters")

    frontend.account.close.click()
    page.locator(frontend.common.user_profile).click()
    page.locator(frontend.common.norm_text_span.format("Log out")).click()


# =============================================================================
# T009 — NAIC Group Code allows only numeric characters
# =============================================================================
def test_verify_NAIC_Group_code_allow_only_Numeric_characters_T009(log, frontend, browser_page):
    page = browser_page

    frontend.auth.log_in()
    log.info("Signed in to Reporting")

    frontend.common.toggle_arrow.hover()
    frontend.common.toggle_arrow.click()
    page.locator(frontend.common.norm_text_span.format("Admin")).click()
    page.locator(frontend.common.norm_text_span.format("Accounts")).click()
    frontend.common.toggle_arrow.click()
    page.locator(frontend.account.account_link.format("Perrknight")).click()
    log.info("Navigated to Account Details Page")

    page.locator(frontend.account.input_edit.format("naicGroupCode")).click()
    valid_code = data.random_digits(4)
    page.locator(frontend.account.input_text).fill(valid_code)
    time.sleep(1)
    frontend.account.save.click()
    log.info(f"Entered NAIC Group Code: {valid_code}")

    saved = page.locator(
        frontend.account.input_edit.format("naicGroupCode")
    ).inner_text()
    assert saved.strip().isdigit(), f"NAIC Group Code should be numeric, got: {saved}"
    log.info("NAIC Group Code accepts only numeric characters — verified")

    page.locator(frontend.common.user_profile).click()
    page.locator(frontend.common.norm_text_span.format("Log out")).click()
