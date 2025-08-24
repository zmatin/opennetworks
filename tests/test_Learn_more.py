import time

import pytest
import requests

from pageObjects.learn_more_PO import LearnMorePO
from pageObjects.main_page_PO import MainPage


@pytest.mark.usefixtures("driver")
class TestMPLearnMore:

    def test_title_page(self, driver):
        main_page = MainPage(driver)
        response = requests.get(main_page.HOME_URL)
        assert response.status_code == 200
        assert main_page.EXPECTED_TITLE in main_page.title_page()

    def test_does_learn_more_button_exist(self, driver):
        lm = LearnMorePO(driver)
        lm.scroll_to(lm.learn_more_locator)

        assert lm.is_learn_more_present(), "❌ Learn More button is not visible on the page"

    def test_click_learn_more_and_navigate(self, driver):
        lm = LearnMorePO(driver)
        lm.click_learn_more()

        # Assert URL contains "learn-more" OR heading is displayed
        assert "learn-more" in driver.current_url or \
               driver.find_element(*lm.express_interest).is_displayed(), \
            "❌ Did not land on the Learn More page"

    def test_provider_option(self, driver):
        lm = LearnMorePO(driver)
        lm.click_learn_more()

        # Ensure Provider option exists and click it
        assert lm.does_provider_exist(), "Provider option not found"
        lm.click_provider()

        # Assert we landed on the Provider page
        assert "provider" in driver.current_url.lower(), "Did not navigate to Provider page"

        # Fill in the form fields
        lm.fill_form(
            email="test@example.com",
            first_name="John",
            last_name="Doe",
            company_name="OpenNetworks Inc"
        )
        time.sleep(5)  # left here for presentation purposes
