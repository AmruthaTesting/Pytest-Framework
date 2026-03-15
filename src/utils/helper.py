import re
import time
from typing import Optional

from playwright.sync_api import Page, Locator, expect

from src.config.logger import logger


class UIHelper:
    def __init__(self, page: Page):
        self.page: Page = page

    # =========================================================================
    # SCROLLING
    # =========================================================================
    def scroll_to_top(self):
        self.page.evaluate("window.scrollTo(0, 0)")
        logger.info("Scrolled to the top of the page.")

    def scroll_to_bottom(self):
        self.page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        logger.info("Scrolled to the bottom of the page.")

    # =========================================================================
    # BASIC UI INTERACTIONS
    # =========================================================================
    def search_list_by_text(self, selector: str, value: str, double: bool = False) -> str:
        """Find a list item containing `value` and click (or double-click) it."""
        element = self.page.locator(selector, has_text=value)
        expect(element).to_be_visible()
        if double:
            element.dblclick()
        else:
            element.click()
        result = element.text_content()
        logger.info(f"Picked list item with text '{value}' (double_click={double}).")
        return result

    def scroll_to_text_value(self, text: str):
        """Scroll until the element with that text is visible then click it."""
        el = self.page.locator(f"text={text}")
        el.scroll_into_view_if_needed()
        el.click()
        logger.info(f"Scrolled to and clicked text '{text}'.")

    # =========================================================================
    # LOCATOR GETTERS
    # =========================================================================
    def get_column_header(self, name: str) -> Locator:
        loc = self.page.locator(
            f"//th[@role='columnheader' and normalize-space()=\"{name}\"]"
        )
        logger.info(f"Prepared locator for column header '{name}'.")
        return loc

    def get_tab(self, name: str) -> Locator:
        loc = self.page.locator(
            f'//*[@role="tablist"]//span[text()="{name}"]'
        )
        logger.info(f"Prepared locator for tab '{name}'.")
        return loc

    def get_cell(self, row: int, column: int) -> Locator:
        loc = self.page.locator(f"//tbody//tr[{row}]//td[{column}]")
        logger.info(f"Prepared locator for cell at row {row}, column {column}.")
        return loc

    # =========================================================================
    # TABLE HELPERS
    # =========================================================================
    def assert_cell_value_by_column_name(
        self,
        column_name: str,
        expected_value: str,
        row_index: int = 1,
        table_locator: Optional[Locator] = None,
    ) -> None:
        """Assert the value of a table cell identified by column name and row index."""
        scope = table_locator or self.page.locator("//table")

        headers = scope.locator("//th[@role='columnheader'] | //th")
        header_count = headers.count()
        if header_count == 0:
            raise AssertionError("No headers found in the table")

        column_index = None
        for i in range(header_count):
            header_text = (headers.nth(i).inner_text() or "").strip()
            if header_text == column_name:
                column_index = i + 1
                break

        if column_index is None:
            raise AssertionError(f"Column '{column_name}' not found")

        cell   = scope.locator(f"xpath=.//tbody/tr[{row_index}]/td[{column_index}]")
        actual = (cell.inner_text() or "").strip()
        assert actual == expected_value, (
            f"Cell [{row_index}, '{column_name}']: expected '{expected_value}', got '{actual}'"
        )
        logger.info(
            f"Asserted cell [{row_index}, '{column_name}'] == '{expected_value}'. ✓"
        )

    def is_value_in_column(
        self,
        column_name: str,
        expected_value: str,
        partial_match: bool = False,
        require_all: bool = False,
        table_locator: Optional[Locator] = None,
    ) -> bool:
        """Return True if any (or all) cells in the column match expected_value."""
        scope = table_locator or self.page.locator("//table")

        headers      = scope.locator("//th[@role='columnheader'] | //th")
        header_count = headers.count()

        column_index = None
        for i in range(header_count):
            if (headers.nth(i).inner_text() or "").strip() == column_name:
                column_index = i + 1
                break
        if column_index is None:
            raise Exception(f"Column '{column_name}' not found.")

        cells      = scope.locator(f"xpath=//tr/td[{column_index}]")
        cell_count = cells.count()

        def matches(value: str) -> bool:
            return (expected_value in value) if partial_match else (expected_value == value)

        if expected_value is None:
            result = all(
                (cells.nth(i).inner_text() or "").strip() != ""
                for i in range(cell_count)
            )
        elif not require_all:
            result = any(
                matches((cells.nth(i).inner_text() or "").strip())
                for i in range(cell_count)
            )
        else:
            result = all(
                matches((cells.nth(i).inner_text() or "").strip())
                for i in range(cell_count)
            )

        logger.info(
            f"Checked column '{column_name}' for '{expected_value}' "
            f"(partial={partial_match}, require_all={require_all}): {result}."
        )
        return result

    # =========================================================================
    # EXPECT / ASSERT HELPERS
    # =========================================================================
    def expect_value_contains(
        self, locator: Locator, part: str,
        ignore_case: bool = True, timeout: int = 5000,
    ):
        flags   = re.IGNORECASE if ignore_case else 0
        pattern = re.compile(rf".*{re.escape(part)}.*", flags)
        expect(locator).to_have_value(pattern, timeout=timeout)
        logger.info(f"Assertion passed: value contains '{part}'.")

    def expect_value_startswith(
        self, locator: Locator, prefix: str,
        ignore_case: bool = True, timeout: int = 5000,
    ):
        flags   = re.IGNORECASE if ignore_case else 0
        pattern = re.compile(rf"{re.escape(prefix)}.*", flags)
        expect(locator).to_have_value(pattern, timeout=timeout)
        logger.info(f"Assertion passed: value starts with '{prefix}'.")

    def expect_value_endswith(
        self, locator: Locator, suffix: str,
        ignore_case: bool = True, timeout: int = 5000,
    ):
        flags   = re.IGNORECASE if ignore_case else 0
        pattern = re.compile(rf".*{re.escape(suffix)}$", flags)
        expect(locator).to_have_value(pattern, timeout=timeout)
        logger.info(f"Assertion passed: value ends with '{suffix}'.")

    def expect_value_equals_ignoring_space(
        self, locator: Locator, value: str, timeout: int = 5000,
    ):
        normalized = " ".join(value.split())
        expect(locator).to_have_value(normalized, timeout=timeout)
        logger.info("Assertion passed: value equals expected (ignoring extra spaces).")

    def click_ready(self, locator: Locator, timeout: int = 15000):
        """Wait until locator is visible AND enabled, then click."""
        expect(locator).to_be_visible(timeout=timeout)
        expect(locator).to_be_enabled(timeout=timeout)
        locator.click()
        logger.info("Clicked element after confirming it is ready.")
