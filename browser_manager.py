from dataclasses import dataclass
from playwright.sync_api import sync_playwright

@dataclass()
class BrowserManager:
    playwright: sync_playwright
    base_url: str
    browser = None
    page = None

    def initialize_browser(self) -> None:
        '''
        This method is used to open the browser with the Google page.
        '''
        try:
            # Launch the browser
            self.browser = self.playwright.chromium.launch(headless=False)
            # Create a new page
            self.page = self.browser.new_page()
            # Navigate to the base URL
            self.page.goto(self.base_url, timeout=150000)
            # Wait for the search textarea to appear
            self.page.wait_for_selector("xpath=//textarea[@title='Search']", timeout=100000)

        except Exception as e:
            # If any error occurs during initialization, raise an exception
            raise RuntimeError(f"Error occurred during browser initialization: {str(e)}")
