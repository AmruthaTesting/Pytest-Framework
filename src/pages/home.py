import os
import tempfile

from playwright.sync_api import expect

from src.config.logger import logger
from src.utils.helper import UIHelper


class HomeElementsPage:
    def __init__(self, page):
        self.page = page
        self.ui = UIHelper(page)

        # ── Home / Dashboard ─────────────────────────────────────────────────
        self.process_type_dropdown = page.locator(
            '#processType span[role="combobox"]'
        )
        self.stat_file_process_type = page.locator(
            'div#fileUploadProcess.p-dropdown'
        )
        self.panel = page.locator('.p-dropdown-panel:visible')

        # ── Account information block ─────────────────────────────────────────
        self.account_name_block = page.locator(
            '//span[normalize-space()="Account Name:"]'
            '/ancestor::div[contains(@class,"content-wrapper")][1]'
        )

        # ── Start File Runs button ────────────────────────────────────────────
        self.Stat_file = page.locator(
            '//button[contains(@label,"Start File Runs")]'
        )

    # ── Actions ──────────────────────────────────────────────────────────────
    def select_process_type(self, value: str):
        self.process_type_dropdown.click()
        self.page.get_by_role("option", name=value).click()

    def open_file_upload_process_dropdown(self):
        self.stat_file_process_type.click()
        self.panel.wait_for(state="visible")

    def dropdown_option(self, value: str):
        panel = self.page.locator(".p-dropdown-panel:visible")
        return panel.locator('li[role="option"]', has_text=value)
