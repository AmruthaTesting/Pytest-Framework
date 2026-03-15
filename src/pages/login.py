import time

from playwright.sync_api import expect

from src.config import env
from src.config.logger import logger
from src.pages.common import CommonElementsPage
from src.utils.helper import UIHelper


class LoginPage:
    def __init__(self, page):
        self.page = page
        self.common = CommonElementsPage(page)
        self.ui = UIHelper(page)

        # ── Locators ────────────────────────────────────────────────────────
        self.go_to_login = page.locator('//span[normalize-space()="Go to Login"]')
        self.username = page.locator('//input[@formcontrolname="username"]')
        self.email = page.locator('//input[@formcontrolname="username"]')
        self.password = page.locator('//input[@formcontrolname="password"]')
        self.continue_btn = page.locator('//span[normalize-space()="Continue"]')
        self.local_login = page.locator('//span[normalize-space()="Local Login"]')
        self.pk1_cloud_login = page.locator(
            '//span[normalize-space()="Pk1Cloud Login"]'
        )
        self.product_title = page.locator(
            '//img[@src="/assets/logos/Product_Logo.svg"]'
        )
        self.remember_me = page.locator(
            '//label[normalize-space()="Remember me"]'
        )

    # ── Actions ──────────────────────────────────────────────────────────────
    def log_in(self, login=None, password=None):
        login = login or env.USER
        password = password or env.PASSWORD
        expect(self.email).to_be_visible(timeout=10_000)
        self.email.fill(login)
        self.password.fill(password)
        time.sleep(1)
        expect(self.continue_btn).to_be_visible(timeout=10_000)
        self.continue_btn.click()
        logger.info("Logged into Reporting")
