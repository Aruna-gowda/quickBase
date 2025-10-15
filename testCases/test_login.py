import allure
import pytest
from pageObjects.login_page import LoginPage

@pytest.mark.usefixtures("setup_and_teardown", "log_on_failure")
class TestHome:

    @allure.title("User able to login into QuickBase application")
    def test_login_QuickBase(self):
        LoginPage(self.page).login_into_quickbase()