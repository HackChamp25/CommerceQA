import pytest
from playwright.sync_api import Page, expect
from pages.login_page import LoginPage
from utils.test_data_reader import load_test_data

login_test_data = load_test_data("login_data.json")

@pytest.mark.ui
@pytest.mark.smoke
def test_valid_user_login(page: Page):
    login = LoginPage(page)
    login.navigate()
    login.login("standard_user", "secret_sauce")
    expect(page).to_have_url("/inventory.html")
    expect(page.get_by_text("Products")).to_be_visible()

@pytest.mark.ui
@pytest.mark.regression
@pytest.mark.parametrize("test_data", login_test_data, ids=["invalid_user","locked_user"])
def test_invalid_user_login(page: Page,test_data):
    login = LoginPage(page)
    login.navigate()
    login.login(test_data["username"], test_data["password"])
    login.verify_error_message(test_data["expected_error"])
    
