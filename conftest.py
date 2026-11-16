import allure
import pytest
from playwright.sync_api import sync_playwright

from config.setting import Settings
from pages.login_page import LoginPage
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

from pathlib import Path


@pytest.fixture(scope="function")
def context(browser, request):
    """Create a new browser context for each test function"""
    settings = Settings()
    artifact_dir = Path("reports/playwright") / request.node.name.replace("[", "_").replace("]", "_")
    artifact_dir.mkdir(parents=True, exist_ok=True)
    request.node._playwright_artifact_dir = artifact_dir

    context = browser.new_context(
        base_url=settings.base_url,
        record_video_dir=str(artifact_dir),
    )
    context.set_default_timeout(settings.default_timeout)
    context.tracing.start(screenshots=True, snapshots=True, sources=True)
    yield context

    failed = getattr(request.node, "rep_call", None) and request.node.rep_call.failed
    if failed:
        trace_path = artifact_dir / "trace.zip"
        context.tracing.stop(path=str(trace_path))
        print(f"Playwright trace saved: {trace_path}")
        print(f"Open with: .\\venv\\Scripts\\playwright.exe show-trace {trace_path}")
    else:
        context.tracing.stop()

    context.close()

@pytest.fixture(scope="function")
def page(context):
    """Create a new page for each test function"""
    page = context.new_page()
    page.set_default_timeout(Settings().default_timeout)
    yield page
    page.close()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):

    outcome = yield
    report = outcome.get_result()
    setattr(item, f"rep_{report.when}", report)

    if report.when == "call" and report.failed:

        page = item.funcargs.get("page") or item.funcargs.get("authenticated_page")

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

            allure.attach(
                page.screenshot(full_page=True),
                name=f"{item.name}_failure",
                attachment_type=allure.attachment_type.PNG,
            )

            print(
                f"Screenshot saved: {screenshot_path}"
            )

@pytest.fixture()
def authenticated_page(page):
    login_page = LoginPage(page)
    login_page.navigate()
    login_page.login("standard_user", "secret_sauce")
    yield page


from api_clients.booking_api import BookingAPI

@pytest.fixture
def booking_api():
    settings = Settings()
    client = BookingAPI(settings.api_base_url, settings.api_timeout)
    yield client
    client.close()

@pytest.fixture
def authenticated_booking_api(booking_api):

    response = booking_api.authenticate(
        "admin",
        "password123"
    )

    assert response.status_code == 200

    token = response.json()["token"]
    booking_api.set_auth_token(token)

    return booking_api