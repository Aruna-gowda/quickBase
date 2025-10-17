import allure
import time
from playwright.sync_api import Page, expect
from playwright.sync_api import TimeoutError, Error


class BasePage:
    def __init__(self, page: Page):
        self.page = page

    # ---------- Mask Sensitive Data ----------
    @staticmethod
    def mask_sensitive(field_name: str, value: str) -> str:
        """Mask sensitive information like passwords or tokens."""
        if field_name and any(k in field_name.lower() for k in ["password", "pwd", "secret", "token", "appassword"]):
            return "********"
        return value

    # ---------- Wait for Element ----------
    def _wait_for_element(self, locator, timeout=5000):
        """Wait for element to be visible (supports both string & Locator)."""
        if isinstance(locator, str):
            element = self.page.locator(locator).first
        else:
            element = locator.first
        element.wait_for(state="visible", timeout=timeout)
        return element

    # ---------- Click ----------
    def click(self, locator, field_name: str = None, timeout=5000, retries=1):
        """Click element (auto-waits, supports string or Locator, retries once on failure)."""
        with allure.step(f"Click on element - {field_name}"):
            attempt = 0
            while attempt <= retries:
                try:
                    element = self._wait_for_element(locator, timeout)
                    element.click()
                    return
                except Exception as e:
                    if attempt < retries:
                        time.sleep(1)
                        attempt += 1
                    else:
                        raise AssertionError(f"Click failed on '{field_name}' after {retries + 1} attempts: {e}")

    # ---------- Type ----------
    def type(self, locator, text: str, field_name: str = None, timeout=5000, retries=1):
        """Type text (auto-waits, supports string or Locator, retries once on failure)."""
        step_name = field_name if field_name else locator
        display_text = self.mask_sensitive(step_name, text)
        with allure.step(f"Type value '{display_text}' into {step_name} input field"):
            attempt = 0
            while attempt <= retries:
                try:
                    element = self._wait_for_element(locator, timeout)
                    element.fill(text)
                    return
                except Exception as e:
                    if attempt < retries:
                        time.sleep(1)
                        attempt += 1
                    else:
                        raise AssertionError(f"Typing failed in '{field_name}' after {retries + 1} attempts: {e}")

    # ---------- Navigate ----------
    def go_to_url(self, url: str):
        """Navigate to a specific URL."""
        with allure.step(f"Navigating to {url}"):
            try:
                self.page.goto(url)
            except Exception as e:
                raise AssertionError(f"Navigation failed for '{url}': {e}")

    # ---------- Validation ----------
    @allure.step("Validate condition")
    def validation(self, actual, expected):
        """Generic assertion with Allure log."""
        with allure.step(f"Validating: expected='{expected}', actual='{actual}'"):
            try:
                assert expected in actual, f"Validation failed: Expected {expected}, got {actual}"
            except AssertionError as e:
                raise e

    # ---------- Element Presence Check ----------
    @allure.step("Check if element is present")
    def is_element_present(self, locator, timeout=3000) -> bool:
        try:
            if isinstance(locator, str):
                self.page.locator(locator).first.wait_for(state="visible", timeout=timeout)
            else:
                locator.first.wait_for(state="visible", timeout=timeout)
            return True
        except TimeoutError:
            return False

    @staticmethod
    def is_element_not_present(page, locator, timeout=3000) -> bool:
       
        try:
            # Handle both string and Locator types
            element = page.locator(locator).first if isinstance(locator, str) else locator.first
            element.wait_for(state="visible", timeout=timeout)

            # If element becomes visible, it is present (so return False)
            print(f"[INFO] Element found (should not be present): {locator}")
            return False

        except TimeoutError:
            print(f"[INFO] Element not present as expected: {locator}")
            return True

        except Error as e:
            print(f"[ERROR] Error while verifying element absence: {e}")
            return True
        # -------------------------------------------------------------------------

    def verify_value_in_table(self, table_locator: str, value: str, timeout: int = 10000, assert_on_fail: bool = False) -> bool:
        """
        Waits for the table to load completely and verifies if a given value is present in any row.

        Args:
            table_locator (str): CSS or XPath locator for the table.
            value (str): Text value to search for in the table.
            timeout (int, optional): Max wait time in milliseconds for the table to load. Defaults to 10000 (10s).
            assert_on_fail (bool, optional): If True, raises AssertionError when value not found.

        Returns:
            bool: True if value is found in table, False otherwise.
        """
        try:
            # ✅ Wait for table to load & become visible
            table = self.page.locator(table_locator)
            expect(table).to_be_visible(timeout=timeout)
            self.page.wait_for_load_state("networkidle")

            # ✅ Get all rows
            rows = table.locator("tbody tr")
            row_count = rows.count()

            # ✅ Iterate through rows to find the value
            for i in range(row_count):
                row_text = rows.nth(i).text_content().strip()
                if value.lower() in row_text.lower():
                    print(f"✅ Value '{value}' found in row {i+1}")
                    return True

            # ✅ Not found
            print(f"❌ Value '{value}' not found in the table.")
            if assert_on_fail:
                raise AssertionError(f"Value '{value}' not found in table.")
            return False

        except TimeoutError:
            print("⚠️ Table did not load within the given timeout.")
            if assert_on_fail:
                raise AssertionError("Table did not load within timeout period.")
            return False
   
    @allure.step("Click element in table row where '{search_text}' is found")
    def click_element_in_table(self, table_locator: str, search_text: str, element_type: str = "button", element_name: str = None):
        table = self.page.locator(table_locator)
        table.wait_for(state="visible", timeout=10000)

        row_locator = f"{table_locator} tr" if not table_locator.strip().startswith("//") else f"{table_locator}//tr"
        rows = self.page.locator(row_locator)
        row_count = rows.count()
        if row_count == 0:
            raise AssertionError("❌ No rows found in the table!")

        found = False
        for i in range(row_count):
            row = rows.nth(i)
            row_text = row.inner_text().strip()
            if search_text.lower() in row_text.lower():
                found = True
                print(f"✅ Found '{search_text}' in row {i+1}")
                row.scroll_into_view_if_needed()

                if element_type == "checkbox":
                    row.locator("input[type='checkbox']").check()
                elif element_type == "button":
                    if element_name:
                        row.get_by_role("button", name=element_name).click()
                    else:
                        row.locator("button").first.click()
                elif element_type == "link":
                    if element_name and "delete" in element_name.lower():
                        row.locator("a[title='Permanently delete this table']").click()
                    elif element_name:
                        row.locator(f"a[title*='{element_name}']").click()
                    else:
                        row.locator("a").last.click()
                else:
                    raise ValueError("Unsupported element type. Use 'button', 'link', or 'checkbox'.")
                break

        if not found:
            raise AssertionError(f"❌ Value '{search_text}' not found in the table.")

