import os
import tempfile

from playwright.sync_api import expect

from src.config.logger import logger
from src.utils.helper import UIHelper


class CommonElementsPage:
    def __init__(self, page):
        self.page = page
        self.ui = UIHelper(page)

        # ── Generic XPath templates ──────────────────────────────────────────
        # Use .format("YourText") to fill in the value
        # Example: page.locator(frontend.common.norm_text_span.format("Admin")).click()
        self.normalize_text = '//*[normalize-space()="{}"]'
        self.norm_text_span = '//span[normalize-space()="{}"]'
        self.contains_text = '//*[contains(text(),"{}")]'
        self.span_contains = '//span[contains(text(),"{}")]'
        self.normalize_label = '//label[normalize-space()="{}"]'
        self.p_norm_space = '//p[normalize-space()="{}"]'
        self.following_sibl = '//*[normalize-space()="{}"]/following-sibling::*[1]'

        # ── Navigation arrows ────────────────────────────────────────────────
        self.Right_arrow = page.locator(
            '//i[contains(@class, "icon-arrow-right")]'
        )
        self.left_arrow = page.locator(
            '//i[@class="icon-arrow-left ng-star-inserted"]'
        )
        self.user_profile = page.locator('//i[@class ="icon-user"]')

        # Matches both collapsed (arrow-right) and expanded (arrow-left) state
        self.toggle_arrow = page.locator(
            '//i[contains(@class,"icon-arrow-right") '
            'or contains(@class,"icon-arrow-left")]'
        )
