import pytest

from playwright.sync_api import sync_playwright

from config.setting import Settings
from utils.logger import configure_logging

configure_logging()

@pytest.fixture(scope="session")
def playwright_instance():
    """Initialize playwright once per test session"""
    with sync_playwright() as playwright:
        yield playwright

@pytest.fixture(scope="session")
def browser(playwright_instance):
    """Initialize the browser once per test session"""
    settings = Settings()
    browser_type = getattr(playwright_instance, settings.browser)
    # Bundled Chromium cannot open a window here: Windows application
    # control blocks that chrome.exe. Installed Chrome can.
    channel = settings.channel
    if settings.browser == "chromium" and not settings.headless and not channel:
        channel = "chrome"
    launch_options = {"headless": settings.headless}
    if channel:
        launch_options["channel"] = channel
    if not settings.headless and settings.slow_mo:
        launch_options["slow_mo"] = settings.slow_mo
    browser = browser_type.launch(**launch_options)
    yield browser
    browser.close() 

@pytest.fixture(scope="function")
def context(browser):
    """Create a new browser context for each test function"""
    settings = Settings()
    context = browser.new_context(base_url=settings.base_url)
    context.set_default_timeout(settings.default_timeout)
    yield context
    context.close()

@pytest.fixture(scope="function")
def page(context):
    """Create a new page for each test function"""
    page = context.new_page()
    page.set_default_timeout(Settings().default_timeout)
    yield page
    page.close()


from pathlib import Path


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):

    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:

        page = item.funcargs.get("page")

        if page:

            screenshot_dir = Path(
                "reports/screenshots"
            )

            screenshot_dir.mkdir(
                parents=True,
                exist_ok=True
            )

            screenshot_path = (
                screenshot_dir / f"{item.name}.png"
            )

            page.screenshot(
                path=str(screenshot_path),
                full_page=True
            )

            print(
                f"Screenshot saved: {screenshot_path}"
            )
