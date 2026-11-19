import os
from pathlib import Path

import allure
import pytest
from playwright.sync_api import sync_playwright

from api_clients.booking_api import BookingAPI
from config.constants import ApiAuth, StatusCode, Users
from config.runtime import CLI, get_cli
from config.setting import Settings
from pages.login_page import LoginPage
from utils.logger import configure_logging

configure_logging()


# ---------------------------------------------------------------------------
# Add new CLI options HERE only. They become global for the entire pytest run.
# dest  -> key used in config.runtime.CLI and os.environ
# name  -> flag passed on the command line
# ---------------------------------------------------------------------------
CLI_OPTIONS = [
    {
        "name": "--app-version",
        "dest": "APP_VERSION",
        "attr": "app_version",
        "default": "v1",
        "choices": ["v1", "v2"],
        "help": "UI/API version (global segregation key)",
    },
    {
        "name": "--env",
        "dest": "ENV",
        "attr": "env",
        "default": "qa",
        "choices": ["qa", "staging", "prod"],
        "help": "Target environment name",
    },
]


def apply_cli_options(parser=None, config=None):
    """Register CLI flags and/or publish them as globals for the whole run.

    - parser -> pytest_addoption
    - config -> pytest_configure (CLI dict + os.environ)
    """
    if parser is not None:
        for option in CLI_OPTIONS:
            kwargs = {
                "action": "store",
                "default": option["default"],
                "help": option.get("help", ""),
            }
            if option.get("choices"):
                kwargs["choices"] = option["choices"]
            parser.addoption(option["name"], **kwargs)
        return

    if config is not None:
        CLI.clear()
        for option in CLI_OPTIONS:
            value = config.getoption(option["name"])
            CLI[option["dest"]] = value
            os.environ[option["dest"]] = str(value)
            setattr(config, option["attr"], value)


def pytest_addoption(parser):
    apply_cli_options(parser=parser)


def pytest_configure(config):
    apply_cli_options(config=config)


@pytest.fixture(scope="session")
def app_version():
    return get_cli("APP_VERSION", "v1")


@pytest.fixture(scope="session")
def env():
    return get_cli("ENV", "qa")


@pytest.fixture(scope="session", autouse=True)
def store_pytest_options(app_version, env, settings):
    """Sanas-style: expose CLI values on pytest module for global access.

    Any file can read: pytest.app_version, pytest.env, pytest.settings
    """
    pytest.app_version = app_version
    pytest.env = env
    pytest.settings = settings
    pytest.base_url = settings.base_url
    pytest.api_base_url = settings.api_base_url


@pytest.fixture(scope="session")
def settings(app_version):
    """Single session Settings built from CLI app version."""
    return Settings(app_version=app_version)


@pytest.fixture(scope="session")
def playwright_instance():
    """Initialize playwright once per test session"""
    with sync_playwright() as playwright:
        yield playwright


@pytest.fixture(scope="session")
def browser(playwright_instance, settings):
    """Initialize the browser once per test session"""
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
def context(browser, request, settings):
    """Create a new browser context for each test function"""
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
def page(context, settings):
    """Create a new page for each test function"""
    page = context.new_page()
    page.set_default_timeout(settings.default_timeout)
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
            screenshot_dir = Path("reports/screenshots")
            screenshot_dir.mkdir(parents=True, exist_ok=True)
            screenshot_path = screenshot_dir / f"{item.name}.png"
            page.screenshot(path=str(screenshot_path), full_page=True)
            allure.attach(
                page.screenshot(full_page=True),
                name=f"{item.name}_failure",
                attachment_type=allure.attachment_type.PNG,
            )
            print(f"Screenshot saved: {screenshot_path}")


@pytest.fixture()
def authenticated_page(page):
    login_page = LoginPage(page)
    login_page.navigate()
    login_page.login(Users.STANDARD["username"], Users.STANDARD["password"])
    yield page


@pytest.fixture
def booking_api(settings):
    client = BookingAPI(settings.api_base_url, settings.api_timeout)
    yield client
    client.close()


@pytest.fixture
def authenticated_booking_api(booking_api):
    response = booking_api.authenticate(
        ApiAuth.ADMIN["username"],
        ApiAuth.ADMIN["password"],
    )
    assert response.status_code == StatusCode.OK
    token = response.json()["token"]
    booking_api.set_auth_token(token)
    return booking_api
