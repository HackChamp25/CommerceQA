import pytest
from playwright.sync_api import Page, expect

@pytest.mark.ui
def test_valid_user_login(page: Page):
    page.goto("/")
    page.get_by_placeholder("Username").fill("standard_user")
    #page.fill("#Username", "standard_user")
    page.get_by_placeholder("Password").fill("secret_sauce")
    page.get_by_role("button", name="Login").click()

    expect(page).to_have_url("/inventory.html")
    expect(page.get_by_text("Products")).to_be_visible()

@pytest.mark.ui
@pytest.mark.regression
def test_invalid_user_login(page: Page):

    page.goto("/")

    page.get_by_placeholder("Username").fill(
        "invalid_user"
    )

    page.get_by_placeholder("Password").fill(
        "wrong_password"
    )

    page.get_by_role(
        "button",
        name="Login"
    ).click()

    # Validate error message
    error_message = page.locator(
        '[data-test="error"]'
    )

    expect(error_message).to_be_visible()

    expect(error_message).to_contain_text(
        "Username and password do not match"
    )
