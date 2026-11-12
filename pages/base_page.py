import logging

from playwright.sync_api import Page, expect

class basePage:

    def __init__(self, page: Page):
        self.page = page
        self.logger = logging.getLogger(__name__)

    def navigate(self, path: str = "/"):
        self.logger.info(f"Navigating to {path}")
        self.page.goto(path)

    def click(self, locator):
        self.logger.info(f"Clicking on element with locator: {locator}")
        locator.click()

    def fill(self, locator, value: str):
        self.logger.info(
            "Entering value into input"
        )
        locator.fill(value)

    def get_text(self, locator) -> str:
        return locator.inner_text()

    def is_visible(self, locator) -> bool:
        return locator.is_visible()

    