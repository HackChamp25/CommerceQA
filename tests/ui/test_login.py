import allure
import pytest
from playwright.sync_api import Page, expect

from pages.login_page import LoginPage
from utils.test_data_reader import load_test_data

login_test_data = load_test_data("login_data.json")

@allure.epic("CommerceQA")
@allure.feature("User Authentication")
@allure.story("Valid Login")
@allure.severity(allure.severity_level.CRITICAL)
@allure.title("Verify successful login with valid credentials")
@allure.description(
    "Verify that a registered user can log in "
    "and access the product inventory page."
)
@pytest.mark.ui
@pytest.mark.smoke
def test_valid_user_login(page: Page):
    with allure.step("Navigate to the login page"):
        login = LoginPage(page)
        login.navigate()
    with allure.step("Login with valid credentials"):
        login.login("standard_user", "secret_sauce")
    with allure.step("Verify successful login"):
        expect(page).to_have_url("/inventory.html")
        expect(page.get_by_text("Products")).to_be_visible()

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
    
