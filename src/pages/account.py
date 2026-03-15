import os
import tempfile
import time

from playwright.sync_api import expect

from src.config.logger import logger
from src.utils.helper import UIHelper
from src.utils import test_data as data


class AccountElementsPage:
    def __init__(self, page):
        self.page = page
        self.ui = UIHelper(page)

        # ── Account dashboard ────────────────────────────────────────────────
        self.Dashboard_Name = '//h1[normalize-space()="{}"]'
        self.account_link   = '//a[normalize-space()="{}"]'
        self.field_name     = '//label[normalize-space()="{}"]'

        # ── Inline edit inputs ───────────────────────────────────────────────
        # Usage: page.locator(frontend.account.input_edit.format('naic')).click()
        self.input_edit = (
            '//app-input-text-editor[@name="{}"]'
            '//div[@class ="editable-field ng-star-inserted"]'
        )
        self.input_text = '//input[contains(@class, "p-inputtext")]'
        self.save        = page.locator('//i[@class="icon-check"]')
        self.close       = page.locator('//i[@class="icon-close"]')

        self.auto_renewal = page.locator(
            '//p-checkbox[contains(@class, "p-element")]'
            '//div[contains(@class, "p-checkbox-box")]'
        )
        self.phone_edit = (
            '//app-inputmask-editor[@name="{}"]'
            '//div[@class="editable-field ng-star-inserted"]'
        )
        self.add_file_process = page.locator('//button[@label="Add File Process"]')

        # ── Tab view ─────────────────────────────────────────────────────────
        self.column_header = '//th[normalize-space()="{}"]'
        self.action        = '//app-account-processes-list//th[contains(text(),"{}")]'
        self.tabs_table    = page.locator('//div[@class ="p-tabview-panels"]')

        # ── Add Account form ─────────────────────────────────────────────────
        self.add_account   = '//button[@type="submit"][@label="Add Account"]'
        self.account_type  = page.locator('//*[@id="partyType"]//p-dropdown')
        self.add_company   = page.locator(
            '//li[@role="option"][@aria-label="Company"]'
        )
        self.input         = '//input[@formcontrolname="{}"]'
        self.state_dropdown = page.locator(
            '//p-dropdown[@id="stateId"]//div[@id="stateId"]'
        )
        self.state_list1   = page.locator('#stateId_list')
        self.save_option   = page.locator('//button[@label="Save"]')
        self.cancel_option = page.locator('//button[@label="Cancel"]')
        self.account_name  = '//label[normalize-space()="{}"]/parent::div//input'

    # ── fill_all_required_fields ─────────────────────────────────────────────
    def fill_all_required_fields(self):
        """Fill NAIC + NAIC Group Code with random digits and save each.
        Returns a dict of the values entered so the test can assert them."""
        inputfields = {}

        # NAIC
        naic_loc = self.page.locator(self.input_edit.format("naic"))
        expect(naic_loc).to_be_visible(timeout=10_000)
        naic_loc.click()
        naic_value = data.random_digits(5)
        self.page.locator(self.input_text).fill(naic_value)
        time.sleep(1)
        self.save.click()
        time.sleep(1)
        inputfields["NAIC"] = naic_value

        # NAIC Group Code
        naic_grp_loc = self.page.locator(self.input_edit.format("naicGroupCode"))
        expect(naic_grp_loc).to_be_visible(timeout=10_000)
        naic_grp_loc.click()
        naic_grp_value = data.random_digits(4)
        self.page.locator(self.input_text).fill(naic_grp_value)
        time.sleep(1)
        self.save.click()
        time.sleep(1)
        inputfields["NAIC_Group"] = naic_grp_value

        return inputfields

    # ── select_random_state ───────────────────────────────────────────────────
    def select_random_state(self):
        """Open state dropdown and pick a random option. Returns selected text."""
        import random
        self.state_dropdown.click()
        options = self.state_list1.locator('li[role="option"]')
        options.first.wait_for()
        index = random.randrange(options.count())
        opt   = options.nth(index)
        value = opt.inner_text().strip()
        opt.click()
        return value

    # ── table helper ──────────────────────────────────────────────────────────
    def table(self, header: str):
        return self.page.locator(
            f'//p-tabpanel[contains(@header,"{header}")]//th'
        )

    def input_to_the_add_account(self, name: str):
        return self.page.locator(self.input.format(name))
