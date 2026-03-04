# conftest.py
import pytest
from playwright.sync_api import Page, expect

@pytest.fixture(scope="function")
def page(page: Page):
    """Extended page fixture with custom settings"""
    # Set default timeout
    page.set_default_timeout(10000)
    
    yield page
    
    # Cleanup
    page.close()

@pytest.hookimpl(tryfirst=True)
def pytest_runtest_makereport(item, call):
    """Take screenshot on test failure"""
    if call.excinfo is not None:
        if "page" in item.funcargs:
            page = item.funcargs["page"]
            screenshot = page.screenshot(full_page=True)
            # Attach screenshot to pytest report
            pytest.fail(f"Test failed. See screenshot.")
