import pytest
from utils.logger import get_logger

# Get the logger
logger = get_logger()


def test_google_homepage(browser):
    """Test to verify that the Google homepage opens correctly and the title contains 'Google'."""

    try:
        # Log the status of the test
        logger.info("Starting test: Verifying Google homepage title.")

        # Assert that the title contains "Google"
        assert "Google" in browser.title, "Google homepage title is not correct."

        # Log success if assertion passes
        logger.info("Google homepage opened successfully and the title contains 'Google'.")

    except AssertionError as e:
        # Log the error if the assertion fails
        logger.error(f"Test failed: {e}")
        raise e  # Re-raise the exception after logging it

    except Exception as e:
        # Catch any other unexpected errors
        logger.error(f"An unexpected error occurred: {e}")
        raise e
