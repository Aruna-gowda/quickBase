import allure
import pytest
from pageObjects.login_page import LoginPage
from pageObjects.Table_page import TablePage

@pytest.mark.usefixtures("setup_and_teardown", "log_on_failure")
class TestTable:

    @allure.title("TC001-User able to login into QuickBase application")
    def test_login_QuickBase(self):
        LoginPage(self.page).login_into_quickbase()

    @allure.title("TC02-verify User is able to click on App settings and table link")
    def test_AppSetting(self):
        TablePage(self.page).click_AppSettings_Table()

    @allure.title("TC03-Create and verify Create a new table in QuickBase")
    def test_NewTable(self):
        TablePage(self.page).create_new_table()

    @allure.title("TC04-Add Label in the new created table")
    def test_Add_NewLabel(self):
        TablePage(self.page).Add_NewLabel()

    @allure.title("TC05-Verify Add Label after adding label")
    def test_Verify_NewLabel(self):
        TablePage(self.page).Verify_NewLabel()

    @allure.title("TC06-Verify Table after adding label")
    def test_Verify_Table(self):
        TablePage(self.page).click_AppSettings_Table()
        TablePage(self.page).Verify_NewTable()

    @allure.title("TC07-Delete the created table")
    def test_Delete_Table(self):
        TablePage(self.page).Delete_Table()

    @allure.title("TC08-Verify Table after deleting label")
    def test_Verify_Table_after_Deleting(self):
        TablePage(self.page).Verify_Table_after_Deleting()
