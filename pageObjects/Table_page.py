import allure
from pageObjects.BasePage import BasePage
from playwright.sync_api import TimeoutError as TError


class TablePage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        

        # ----------------------------locators-------------------------------------------------------
        self.AppSettings = '//*[contains(text(),"App settings")]'
        self.Table_field = '[id="appSettingsNav_tables"]'
        self.NewTable = '[id="newTableMenuButton"]'
        self.FromScratch = '[id="tableFromscratch"]'
        self.TimeCards = "//button[contains(text(),'Time Cards')]"
        self.TableDescription = '[data-test-id="TableDescription"]'
        self.TableName = '[data-test-id="TableName"]'
        self.CreateTable = '[data-test-id="dialogOkButton"]'

        self.new_table_button = self.page.get_by_role("button", name="+ New Table")
        self.from_scratch_link = self.page.get_by_role("link", name="From scratch Design your own")
        self.table_name_field = self.page.get_by_role("textbox", name="Table name")
        self.table_option = self.page.get_by_role("option", name="Customers")
        self.table_description_field = self.page.locator('[data-test-id="TableDescription"]')
        self.dialog_ok_button = self.page.locator('[data-test-id="dialogOkButton"]')

        self.addLabel  = self.page.locator('//div[@class="fieldNameInput__input"]')
        self.Name = self.page.locator('(//b[contains(text(),"Name")])[1]')
        self.AddFileds =page.locator("[data-test-id=\'dialogOkButton\']")
        self.Name_after = self.page.locator('(//div[contains(text(),"Name")])[1]')
        # self.Verify_Table = self.page.locator("//a[@class='HasAutoTip'][normalize-space()='Customers']")
        self.Verify_Table = self.page.locator('//a[contains(text(),"Customers") and @data-tipped="next"]')

        self.Table_checkBox = '(//a[contains(text(),"Customers") and @data-tipped="next"]/preceding::input[@type="checkbox"])[last()]'
        self.DeleteRow = '//a[contains(text(),"Customers") and (@data-tipped="next")]/following::a[@class="RowAction Delete Icon"]'
        self.Yes_Delete = '//input[@name="typeYesField"]"'
        self.Delete_Buttpn = '//button[contains(text(),"Delete Table")]'
        # -------------------------------------------------------------------------------------------

    @allure.step("verify User is able to click on App settings and table link")
    def click_AppSettings_Table(self):
        self.click(self.AppSettings, "AppSettings Button")
        self.click(self.Table_field, "Table Link")


    @allure.step("Create a new table in QuickBase")
    def create_new_table(self, table_name="Customers", description="testing"):
        # Click '+ New Table'
        self.click(self.new_table_button, "'+ New Table' Button")

        # Click 'From scratch' link
        self.click(self.from_scratch_link, "'From scratch Design your own' Link")

        # Fill table name and select option
        self.type(self.table_name_field, table_name, "Table Name Field")
        self.click(self.table_option, f"Table Option - {table_name}")

        # Fill table description
        self.type(self.table_description_field, description, "Table Description Field")

        # Click OK to create table
        self.click(self.dialog_ok_button, "'OK' Button")

    @allure.step("Add Label in the new created table")
    def Add_NewLabel(self):
        self.click(self.addLabel, "Add Label")
        self.type(self.addLabel, "Name", "Name")
        self.click(self.Name, "Name")
        self.click(self.AddFileds, "Add Fields")

    @allure.step("Verify new Label in the new created table")
    def Verify_NewLabel(self):
        self.is_element_present(self.Name_after, "Name after adding label")

    @allure.step("Verify Table after adding label")
    def Verify_NewTable(self):
        self.is_element_present(self.Verify_Table, "Table after adding label")

    @allure.step("Delete the created table")
    def Delete_Table(self):
        try:
            self.page.wait_for_selector(self.Table_checkBox, timeout=5000)
            self.click(self.Table_checkBox, "Table CheckBox")
            self.click(self.DeleteRow, "Delete Row")
            self.page.wait_for_selector("text='Delete this Table?'", timeout=5000)
            self.type(self.Yes_Delete, "YES", "Type Yes to delete")
            self.click(self.Delete_Buttpn, "Delete Button")
        except TError:
            print("No table found to delete.")
    
    @allure.step("Verify Table after deleting label")
    def Verify_Table_after_Deleting(self):
        self.is_element_not_present(self.Verify_Table, "Table after deleting label")    