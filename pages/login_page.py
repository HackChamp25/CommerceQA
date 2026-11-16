from playwright.sync_api import Page, expect

from pages.base_page import basePage


class LoginPage(basePage):
    def __init__(self, page:Page):
        super().__init__(page)
        self.username = page.get_by_placeholder("username")
        self.password = page.get_by_placeholder("password")
        self.login_button = page.get_by_role("button", name="Login")
        self.error_message = page.locator('[data-test="error"]')

    def login(self, username: str, password: str):
        self.fill(self.username, username)
        self.fill(self.password, password)
        self.click(self.login_button)

    def verify_error_message(self, expected_message: str):
        expect(self.error_message).to_be_visible()
        expect(self.error_message).to_contain_text(expected_message)
        
