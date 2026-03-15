import time

from playwright.sync_api import expect

from src.utils import test_data as data


# ---------------------------------------------------------------------------
# Shared helper
# ---------------------------------------------------------------------------
def _go_to_accounts_list(page, frontend, log):
    frontend.auth.log_in()
    log.info("Signed in to Reporting")
    frontend.common.toggle_arrow.hover()
    frontend.common.toggle_arrow.click()
    page.locator(frontend.common.norm_text_span.format("Admin")).click()
    page.locator(frontend.common.norm_text_span.format("Accounts")).click()
    log.info("Navigated to Accounts page")


# =============================================================================
# T018 — Add Account button is visible
# =============================================================================
def test_verify_add_account_button_is_visible_T018(log, frontend, browser_page):
    page = browser_page
    _go_to_accounts_list(page, frontend, log)

    expect(
        page.locator(frontend.account.add_account)
    ).to_be_visible(timeout=10_000)
    log.info("Add Account button is visible")

    page.locator(frontend.common.user_profile).click()
    page.locator(frontend.common.norm_text_span.format("Log out")).click()


# =============================================================================
# T019 — Add Account form opens when button clicked
# =============================================================================
def test_verify_add_account_form_opens_on_click_T019(log, frontend, browser_page):
    page = browser_page
    _go_to_accounts_list(page, frontend, log)

    page.locator(frontend.account.add_account).click()
    log.info("Clicked Add Account button")

    expect(
        page.locator(frontend.common.norm_text_span.format("Add Account"))
    ).to_be_visible(timeout=10_000)
    log.info("Add Account form is visible")

    page.locator(frontend.common.user_profile).click()
    page.locator(frontend.common.norm_text_span.format("Log out")).click()


# =============================================================================
# T020 — Account Type dropdown is visible in form
# =============================================================================
def test_verify_account_type_dropdown_visible_T020(log, frontend, browser_page):
    page = browser_page
    _go_to_accounts_list(page, frontend, log)

    page.locator(frontend.account.add_account).click()
    log.info("Opened Add Account form")

    expect(frontend.account.account_type).to_be_visible(timeout=10_000)
    log.info("Account Type dropdown is visible")

    page.locator(frontend.common.user_profile).click()
    page.locator(frontend.common.norm_text_span.format("Log out")).click()


# =============================================================================
# T021 — Select Company from Account Type dropdown
# =============================================================================
def test_verify_select_company_from_account_type_T021(log, frontend, browser_page):
    page = browser_page
    _go_to_accounts_list(page, frontend, log)

    page.locator(frontend.account.add_account).click()
    log.info("Opened Add Account form")

    frontend.account.account_type.click()
    frontend.account.add_company.click()
    log.info("Selected Company as Account Type")

    expect(
        page.locator(frontend.common.norm_text_span.format("Company"))
    ).to_be_visible()
    log.info("Company account type selected and verified")

    page.locator(frontend.common.user_profile).click()
    page.locator(frontend.common.norm_text_span.format("Log out")).click()


# =============================================================================
# T022 — Cancel closes the form without saving
# =============================================================================
def test_verify_cancel_closes_add_account_form_T022(log, frontend, browser_page):
    page = browser_page
    _go_to_accounts_list(page, frontend, log)

    page.locator(frontend.account.add_account).click()
    log.info("Opened Add Account form")

    frontend.account.cancel_option.click()
    log.info("Clicked Cancel")

    expect(
        page.locator(frontend.account.Dashboard_Name.format("Accounts"))
    ).to_be_visible(timeout=10_000)
    log.info("Cancel works — returned to Accounts list")

    page.locator(frontend.common.user_profile).click()
    page.locator(frontend.common.norm_text_span.format("Log out")).click()


# =============================================================================
# T023 — State dropdown is visible and opens
# =============================================================================
def test_verify_state_dropdown_visible_in_add_account_T023(log, frontend, browser_page):
    page = browser_page
    _go_to_accounts_list(page, frontend, log)

    page.locator(frontend.account.add_account).click()
    frontend.account.account_type.click()
    frontend.account.add_company.click()
    log.info("Selected Company account type")

    expect(frontend.account.state_dropdown).to_be_visible(timeout=10_000)
    frontend.account.state_dropdown.click()
    expect(frontend.account.state_list1).to_be_visible(timeout=10_000)
    log.info("State dropdown opens and options are visible")

    page.keyboard.press("Escape")
    page.locator(frontend.common.user_profile).click()
    page.locator(frontend.common.norm_text_span.format("Log out")).click()


# =============================================================================
# T024 — Random state can be selected from dropdown
# =============================================================================
def test_verify_random_state_can_be_selected_T024(log, frontend, browser_page):
    page = browser_page
    _go_to_accounts_list(page, frontend, log)

    page.locator(frontend.account.add_account).click()
    frontend.account.account_type.click()
    frontend.account.add_company.click()

    selected_state = frontend.account.select_random_state()
    log.info(f"Selected state: {selected_state}")

    assert selected_state, "No state was selected"
    log.info("Random state selection verified")

    page.locator(frontend.common.user_profile).click()
    page.locator(frontend.common.norm_text_span.format("Log out")).click()


# =============================================================================
# T025 — Name field accepts text input
# =============================================================================
def test_verify_name_field_accepts_input_T025(log, frontend, browser_page):
    page = browser_page
    _go_to_accounts_list(page, frontend, log)

    page.locator(frontend.account.add_account).click()
    frontend.account.account_type.click()
    frontend.account.add_company.click()
    log.info("Selected Company account type")

    company_name = f"AutoTest_{data.unique_name()}"
    page.locator(frontend.account.input.format("name")).fill(company_name)
    time.sleep(1)

    actual = page.locator(frontend.account.input.format("name")).input_value()
    assert actual == company_name, \
        f"Name field: expected '{company_name}', got '{actual}'"
    log.info(f"Name field accepted input: {company_name}")

    frontend.account.cancel_option.click()
    page.locator(frontend.common.user_profile).click()
    page.locator(frontend.common.norm_text_span.format("Log out")).click()


# =============================================================================
# T026 — Save button is disabled when required fields are empty
# =============================================================================
def test_verify_save_disabled_when_fields_empty_T026(log, frontend, browser_page):
    page = browser_page
    _go_to_accounts_list(page, frontend, log)

    page.locator(frontend.account.add_account).click()
    log.info("Opened Add Account form")

    assert frontend.account.save_option.is_disabled(), \
        "Save button should be disabled when required fields are empty"
    log.info("Save button is correctly disabled when fields are empty")

    frontend.account.cancel_option.click()
    page.locator(frontend.common.user_profile).click()
    page.locator(frontend.common.norm_text_span.format("Log out")).click()


# =============================================================================
# T027 — Save button enables after required fields are filled
# =============================================================================
def test_verify_save_enabled_after_required_fields_filled_T027(log, frontend, browser_page):
    page = browser_page
    _go_to_accounts_list(page, frontend, log)

    page.locator(frontend.account.add_account).click()
    frontend.account.account_type.click()
    frontend.account.add_company.click()

    company_name = f"AutoTest_{data.unique_name()}"
    page.locator(frontend.account.input.format("name")).fill(company_name)
    time.sleep(1)
    log.info(f"Filled name: '{company_name}'")

    expect(frontend.account.save_option).to_be_enabled(timeout=5_000)
    log.info("Save button enabled after required fields are filled")

    frontend.account.cancel_option.click()
    page.locator(frontend.common.user_profile).click()
    page.locator(frontend.common.norm_text_span.format("Log out")).click()


# =============================================================================
# T028 — Full happy path: Add new Company account
# =============================================================================
def test_verify_add_new_company_account_successfully_T028(log, frontend, browser_page):
    page = browser_page
    _go_to_accounts_list(page, frontend, log)

    page.locator(frontend.account.add_account).click()
    log.info("Opened Add Account form")

    frontend.account.account_type.click()
    frontend.account.add_company.click()
    log.info("Selected Company as Account Type")

    company_name = f"AutoTest_{data.unique_name()}"
    page.locator(frontend.account.input.format("name")).fill(company_name)
    log.info(f"Entered company name: {company_name}")

    selected_state = frontend.account.select_random_state()
    log.info(f"Selected state: {selected_state}")

    frontend.account.save_option.click()
    log.info("Clicked Save")

    expect(
        page.locator(frontend.account.account_link.format(company_name))
    ).to_be_visible(timeout=20_000)
    log.info(f"New account '{company_name}' created and visible in list")

    page.locator(frontend.common.user_profile).click()
    page.locator(frontend.common.norm_text_span.format("Log out")).click()


# =============================================================================
# T029 — Add account with ALL required fields (full form)
# =============================================================================
def test_verify_add_account_with_all_required_fields_led_T029(log, frontend, browser_page):
    page = browser_page

    frontend.auth.log_in()
    log.info("Signed in to Reporting")

    frontend.common.toggle_arrow.hover()
    frontend.common.toggle_arrow.click()
    page.locator(frontend.common.norm_text_span.format("Admin")).click()
    page.locator(frontend.common.norm_text_span.format("Accounts")).click()
    log.info("Navigated to Accounts page")

    page.locator(frontend.account.add_account).click()

    frontend.account.account_type.click()
    frontend.account.add_company.click()
    log.info("Selected Company as Account Type")

    company_name = f"AutoTest_{data.unique_name()}"
    page.locator(frontend.account.input.format("name")).fill(company_name)
    log.info(f"Entered company name: {company_name}")

    # Fill NAIC + NAIC Group Code using the page object method
    input_values = frontend.account.fill_all_required_fields()
    log.info(f"Filled required fields: {input_values}")

    selected_state = frontend.account.select_random_state()
    log.info(f"Selected state: {selected_state}")

    frontend.account.save_option.click()
    log.info("Clicked Save")

    expect(
        page.locator(frontend.account.account_link.format(company_name))
    ).to_be_visible(timeout=20_000)
    log.info(f"Account '{company_name}' created and verified in list")

    page.locator(frontend.common.user_profile).click()
    page.locator(frontend.common.norm_text_span.format("Log out")).click()
