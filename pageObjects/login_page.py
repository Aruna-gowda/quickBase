import allure
from pageObjects.BasePage import BasePage
from utilities import read_otp
from playwright.sync_api import TimeoutError as TError
from utilities.read_config import read_data


class LoginPage(BasePage):
    def __init__(self, page):
        super().__init__(page)

        # ---------- Test Data ----------
        self.url = read_data("url")
        self.username = read_data("Email")
        self.password = read_data("Password")
        self.app_password = read_data("APPPassword")
        

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
        self.page.wait_for_timeout(10000)

        # OTP Handling (optional)
        otp = read_otp.get_latest_otp_email(self.username, self.app_password)
        self.type(self.otp_field, otp, "Verification Code")
        self.click(self.page.locator('[name=\"SignIn\"]'), "Sign In Button")
        self.page.wait_for_timeout(5000)

        # Validation example
        # self.validation(self.page.title(), "Automation")
        self.validation(self.page.title(), "Project Manager")
