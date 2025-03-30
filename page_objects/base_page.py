import time
import os
import traceback
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    TimeoutException, NoSuchElementException, ElementClickInterceptedException,
    StaleElementReferenceException, WebDriverException
)
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from utils.logger import get_logger  # Import the centralized self.logger

class BasePage:
    """A robust and optimized BasePage for all page interactions."""

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
        self.logger=get_logger()

    # ✅ Safe Click with Retry Mechanism
    def click(self, locator, retries=2):
        """Click an element with retry logic to handle temporary failures."""
        for attempt in range(retries):
            try:
                element = self.wait.until(EC.element_to_be_clickable(locator))
                element.click()
                self.logger.info(f"✅ Clicked on: {locator}")
                return
            except (TimeoutException, ElementClickInterceptedException, StaleElementReferenceException) as e:
                self.logger.warning(f"⚠️ Click failed ({attempt + 1}/{retries}) for {locator} - {e}")
                time.sleep(1)  # Small delay before retry
        self.logger.error(f"❌ Click failed for {locator} after {retries} retries")
        raise Exception(f"Click failed for {locator}")

    # ✅ Safe Text Entry
    def enter_text(self, locator, text, clear=True):
        """Enter text safely into an input field."""
        try:
            element = self.wait.until(EC.presence_of_element_located(locator))
            if clear:
                element.clear()
            element.send_keys(text)
            self.logger.info(f"✅ Entered text '{text}' in {locator}")
        except TimeoutException:
            self.logger.error(f"❌ Timeout: Unable to enter text in {locator}")
            raise Exception(f"Timeout: Unable to enter text in {locator}")

    # ✅ Retrieve Text Safely
    def get_text(self, locator):
        """Get text from an element safely."""
        try:
            element = self.wait.until(EC.visibility_of_element_located(locator))
            text = element.text
            self.logger.info(f"✅ Retrieved text '{text}' from {locator}")
            return text
        except TimeoutException:
            self.logger.error(f"❌ Timeout: Unable to get text from {locator}")
            raise Exception(f"Timeout: Unable to get text from {locator}")

    # ✅ Check if Element is Present
    def is_element_present(self, locator):
        """Check if an element is present on the page."""
        try:
            self.driver.find_element(*locator)
            self.logger.info(f"✅ Element {locator} is present")
            return True
        except NoSuchElementException:
            self.logger.warning(f"⚠️ Element {locator} is NOT present")
            return False

    # ✅ Safe Scrolling
    def scroll_to_element(self, locator):
        """Scroll the page to make an element visible."""
        try:
            element = self.wait.until(EC.presence_of_element_located(locator))
            self.driver.execute_script("arguments[0].scrollIntoView();", element)
            self.logger.info(f"✅ Scrolled to element: {locator}")
        except TimeoutException:
            self.logger.error(f"❌ Timeout: Unable to scroll to {locator}")
            raise Exception(f"Timeout: Unable to scroll to {locator}")

    # ✅ Scroll to Bottom of the Page
    def scroll_to_bottom(self):
        """Scroll to the bottom of the page."""
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        self.logger.info("✅ Scrolled to the bottom of the page")

    # ✅ Take Screenshot on Failure
    def take_screenshot(self, filename="screenshot.png"):
        """Capture a screenshot and save it to the logs directory."""
        screenshot_path = os.path.join("logs", filename)
        self.driver.save_screenshot(screenshot_path)
        self.logger.info(f"📸 Screenshot saved at {screenshot_path}")

    # ✅ Handle JavaScript Alerts
    def handle_alert(self, accept=True):
        """Handle browser alert pop-ups (Accept/Dismiss)."""
        try:
            alert = self.driver.switch_to.alert
            alert_text = alert.text
            if accept:
                alert.accept()
                self.logger.info(f"✅ Alert accepted: {alert_text}")
            else:
                alert.dismiss()
                self.logger.info(f"✅ Alert dismissed: {alert_text}")
            return alert_text
        except WebDriverException:
            self.logger.warning("⚠️ No alert found")
            return None

    # ✅ Refresh Page
    def refresh_page(self):
        """Refresh the current page."""
        self.driver.refresh()
        self.logger.info("✅ Page refreshed successfully")

    # ✅ Wait for Page to Load Completely
    def wait_for_page_load(self, timeout=10):
        """Wait for the page to fully load."""
        try:
            WebDriverWait(self.driver, timeout).until(
                lambda driver: driver.execute_script("return document.readyState") == "complete"
            )
            self.logger.info("✅ Page fully loaded")
        except TimeoutException:
            self.logger.error("❌ Timeout: Page did not load completely")

    # ✅ Execute JavaScript
    def execute_script(self, script, *args):
        """Execute JavaScript on the page."""
        result = self.driver.execute_script(script, *args)
        self.logger.info(f"✅ Executed JavaScript: {script}")
        return result
