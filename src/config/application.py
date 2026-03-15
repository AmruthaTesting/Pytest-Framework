from src.pages.login import LoginPage
from src.pages.account import AccountElementsPage
from src.pages.home import HomeElementsPage
from src.pages.common import CommonElementsPage
from src.utils.helper import UIHelper
from src.config.logger import logger
from src.config import env


class Frontend:
    """
    Single facade object that bundles every page object.
    Injected into every test via the `frontend` fixture in conftest.py.

    In tests, access pages like:
        frontend.auth.log_in()
        frontend.common.toggle_arrow.click()
        frontend.account.fill_all_required_fields()
        frontend.home.Stat_file.click()
        frontend.helper.assert_cell_value_by_column_name('Status', 'Active')
    """

    def __init__(self, page):
        self.page = page

        self.auth = LoginPage(page)
        self.home = HomeElementsPage(page)
        self.common = CommonElementsPage(page)
        self.account = AccountElementsPage(page)
        self.resolution = env.RESOLUTION
        self.helper = UIHelper(page)

        logger.debug("Frontend initialized")

    def open_url(self, url=None):
        self.page.goto(url or env.URL)

    def get_current_url(self):
        return self.page.url

    def set_viewport_size(self, width, height):
        self.page.context.set_viewport_size({"width": width, "height": height})
