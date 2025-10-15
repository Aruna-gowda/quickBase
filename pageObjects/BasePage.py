import allure
import time
from playwright.sync_api import Page
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