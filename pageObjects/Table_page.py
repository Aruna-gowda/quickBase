import allure
from pageObjects.BasePage import BasePage
from playwright.sync_api import TimeoutError as TError



class TablePage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        
        self.Table_name = "Automation"
        self.field_name = "Name"

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
        self.SingleRecord = '[data-test-id="SingleRecordInput"]'
        self.table_option = self.page.get_by_role("option", name="Customers")
        self.table_description_field = self.page.locator('[data-test-id="TableDescription"]')
        self.dialog_ok_button = self.page.locator('[data-test-id="dialogOkButton"]')

        self.addLabel ='//*[(contains(text(),"Add a label")) and (@class="css-12f1u7m fieldNameInput__placeholder")]'
        self.Name = self.page.locator('(//b[contains(text(),"Name")])[1]')
        self.AddFileds =page.locator("[data-test-id=\'dialogOkButton\']")
        self.Verify_Table = self.page.locator('//a[contains(text(),"Customers") and @data-tipped="next"]')
        self.table_Fileds = "#fieldsTable"
        self.appTable="#appTablesListTable"

# ----------------------------------methods-------------------------------------------------------

    @allure.step("verify User is able to click on App settings and table link")
    def click_AppSettings_Table(self):
        self.click(self.AppSettings, "AppSettings Button")
        self.click(self.Table_field, "Table Link")

    @allure.step("Create a new table in QuickBase")
    def create_new_table(self):
        # Click '+ New Table'
        self.click(self.new_table_button, "'+ New Table' Button")

        # Click 'From scratch' link
        self.click(self.from_scratch_link, "'From scratch Design your own' Link")

        # Fill table name and select option
        self.type(self.table_name_field, self.Table_name, "Table Name Field")
        self.type(self.SingleRecord, self.Table_name, "Single Record Field")

        # Fill table description
        self.type(self.table_description_field, "testing", "Table Description Field")

        # Click OK to create table
        self.click(self.dialog_ok_button, "'OK' Button")


    @allure.step("Add Label in the new created table")
    def Add_NewLabel(self):
        # Click on the "Add a label" placeholder
        self.page.locator("div.fieldNameInput__placeholder", has_text="Add a label").click()
        # Type into the now-active editable field
        self.page.keyboard.type("Name")
        self.click(self.Name, "Name")
        self.click(self.AddFileds, "Add Fields")

    @allure.step("Verify new Label in the new created table")
    def Verify_NewLabel(self):
        self.verify_value_in_table(self.table_Fileds, self.field_name, assert_on_fail=True)
        
    @allure.step("Verify Table after adding label")
    def Verify_NewTable(self):
        self.verify_value_in_table(self.appTable, self.Table_name, assert_on_fail=True)

    @allure.step("Delete the created table")
    def Delete_Table(self):
        self.click_element_in_table(self.appTable, self.Table_name, element_type="checkbox")
        self.click_element_in_table(self.appTable, self.Table_name, element_type="link")
        self.confirm_table_delete()

    @allure.step("Confirm table deletion")
    def confirm_table_delete(self):
        dialog = self.page.locator("div#dialogDeleteTable")
        dialog.wait_for(state="visible", timeout=10000)

        # Type YES
        self.page.locator("input#typeYesField").fill("YES")

        # Click Delete
        self.page.locator("button:has-text('Delete Table')").click()

        # Wait for dialog to close
        dialog.wait_for(state="hidden", timeout=10000)

    
    @allure.step("Verify Table after deleting label")
    def Verify_Table_after_Deleting(self):
        self.page.wait_for_timeout(3000)  # Wait for 2 seconds to ensure table is deleted
        is_present = self.verify_value_in_table(self.appTable, self.Table_name)
        assert is_present==False, f"Table name '{self.Table_name}' found in the table after deletion"