import allure
import pytest
from allure_commons.types import AttachmentType
from playwright.sync_api import sync_playwright


@pytest.fixture(scope='class')
def setup_and_teardown(request):
    """Launch browser and create page once per test class"""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, slow_mo=500)
        page = browser.new_page()

        # Attach page object to the class so all tests can access it
        if request.cls is not None:
            request.cls.page = page

        yield page

        page.close()
        browser.close()


@pytest.fixture()
def log_on_failure(request, setup_and_teardown):
    """Capture screenshot if test fails"""
    yield
    item = request.node
    if hasattr(item, 'rep_call') and item.rep_call.failed:
        page = setup_and_teardown
        allure.attach(
            page.screenshot(),
            name="failed_test",
            attachment_type=AttachmentType.PNG
        )


@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item, call):
    """Hook to access test result (pass/fail)"""
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)
    return rep


@pytest.fixture
def page(setup_and_teardown):
    """Provide page fixture for backward compatibility"""
    return setup_and_teardown
