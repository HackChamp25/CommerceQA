import pytest
from playwright.sync_api import Page, expect
from pages.login_page import LoginPage

@pytest.mark.ui
def test_valid_user_login(page: Page):
    login = LoginPage(page)
    login.navigate()
    login.login("standard_user", "secret_sauce")
    expect(page).to_have_url("/inventory.html")
    expect(page.get_by_text("Products")).to_be_visible()

@pytest.mark.ui
@pytest.mark.regression
def test_invalid_user_login(page: Page):
    login = LoginPage(page)
    login.navigate()
    login.login("invalid_user", "invalid_password")
    login.verify_error_message("Epic sadface: Username and password do not match any user in this service")
