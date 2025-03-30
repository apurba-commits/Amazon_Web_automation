import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from utils.logger import get_logger
from selenium.common.exceptions import WebDriverException

logger = get_logger()

@pytest.fixture
def browser():
    logger.info("Starting the browser setup...")

    try:
        # Use webdriver_manager to automatically fetch the correct chromedriver
        driver_path = "C:/Users/Apurba2.Dey/Downloads/chromedriver-win64 (1)/chromedriver-win64/chromedriver.exe"  # Replace with your actual path
        service = Service(driver_path)
        driver = webdriver.Chrome(service=service)  # Launch Chrome    # Launch Chrome with the correct driver
        driver.implicitly_wait(10)  # Wait for elements to load
        logger.info("Navigating to Google homepage")
        driver.get("https://www.google.com")

        yield driver  # Return driver instance to the test
    except WebDriverException as e:
        logger.error(f"Failed to initialize the browser or load the page: {e}")
        pytest.fail(f"Test failed due to WebDriverException: {e}")
    finally:
        if 'driver' in locals():
            driver.quit()
            logger.info("Browser closed after the test.")
