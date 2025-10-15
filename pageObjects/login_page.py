import allure
from pageObjects.BasePage import BasePage
from utilities import ReadConfigurations, config
from playwright.sync_api import TimeoutError as TError


class LoginPage(BasePage):
    def __init__(self, page):
        super().__init__(page)

        # ---------- Test Data ----------
        self.url = ReadConfigurations.read_configuration("basic info", "url")
        self.username = ReadConfigurations.read_configuration("basic info", "Username")
        self.password = ReadConfigurations.read_configuration("basic info", "Password")
        self.app_password = ReadConfigurations.read_configuration("basic info", "APPPassword")

        # ---------- Locators ----------
        self.username_field = self.page.locator('[name="loginid"]')
        self.password_field = self.page.locator('[name="password"]')
        self.signin_button = self.page.get_by_role("button", name="Sign in")
        self.otp_field = self.page.locator('[name="TwoStepCode"]')

    @allure.step("Login into QuickBase application")
    def login_into_quickbase(self):
        # Navigate to URL
        self.go_to_url(self.url)

        # Handle optional SSO popup
        sso_popup = self.page.locator("//*[contains(text(),'Do you have a Quickbase single sign-on (SSO) account?')]")
        try:
            if sso_popup.is_visible(timeout=3000):
                self.click(self.page.locator('[id=\"quickbaseSignin\"]'), "Quickbase SSO Signin")
        except TError:
            pass

        # Enter credentials
        self.type(self.username_field, self.username, "Username")
        self.type(self.password_field, self.password, "Password")
        self.click(self.signin_button, "Sign In Button")
        self.page.wait_for_timeout(5000)

        # OTP Handling (optional)
        otp = config.get_latest_otp_email(self.username, self.app_password)
        self.type(self.otp_field, otp, "Verification Code")
        self.click(self.page.locator('[name=\"SignIn\"]'), "Sign In Button")
        self.page.wait_for_timeout(5000)

        # Validation example
        # self.validation(self.page.title(), "Automation")
        self.validation(self.page.title(), "Simple Project Manager")
