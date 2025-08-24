import pytest
import requests
from selenium.common import TimeoutException
from selenium.webdriver import ActionChains

from pageObjects.main_page_PO import MainPage


@pytest.mark.usefixtures("driver")
class TestMainPage:

    def test_title_page(self, driver):
        main_page = MainPage(driver)
        response = requests.get(main_page.HOME_URL)
        assert response.status_code == 200
        assert main_page.EXPECTED_TITLE in main_page.title_page()

    def test_home_url(self, driver):
        main_page = MainPage(driver)
        assert main_page.HOME_URL in main_page.get_url()

    def test_logo_is_displayed(self, driver):
        main_page = MainPage(driver)
        assert main_page.is_logo_present() is True

    def test_nav_menu_items_exist(self, driver):
        """Verify all main nav menu items are displayed"""
        main_page = MainPage(driver)
        nav_items = {
            "Home": main_page.nav_menu_home(),
            "About Us": main_page.nav_menu_about_us(),
            "Providers": main_page.nav_menu_providers(),
            "Employers": main_page.nav_menu_employers()
        }
        for name, element in nav_items.items():
            assert element.is_displayed(), f"Nav menu item '{name}' is not displayed"

    def test_more_button_exists(self, driver):
        """Verify the 'More' menu button exists"""
        main_page = MainPage(driver)
        assert main_page.does_nav_more_button_exist(), "'More' button does not exist"

    def test_more_button_click_dropdown(self, driver):
        """Verify clicking 'More' opens the dropdown menu and it has 3 options"""
        main_page = MainPage(driver)

        if main_page.does_nav_more_button_exist():
            # Click 'More' and wait for dropdown
            dropdown_visible = main_page.move_and_click_more()
            assert dropdown_visible, "Dropdown did not appear after clicking 'More'"

            # Verify all three options exist
            try:
                faq = main_page.wait.until(
                    lambda d: d.find_element(*main_page.faq_locator)
                )
                blog = main_page.wait.until(
                    lambda d: d.find_element(*main_page.blog_locator)
                )
                careers = main_page.wait.until(
                    lambda d: d.find_element(*main_page.careers_locator)
                )
            except TimeoutException:
                pytest.fail("One or more dropdown options were not found")

            # Check all options are displayed
            assert faq.is_displayed(), "FAQ option is not displayed"
            assert blog.is_displayed(), "Blog option is not displayed"
            assert careers.is_displayed(), "Careers option is not displayed"

        else:
            pytest.skip("'More' button does not exist, skipping dropdown test")

    def test_highlight_feature_dropdown(self, driver):
        """Verify hovering over each 'More' dropdown option highlights it"""
        main_page = MainPage(driver)

        if main_page.does_nav_more_button_exist():
            # Click 'More' and wait for dropdown
            dropdown_visible = main_page.move_and_click_more()
            assert dropdown_visible, "Dropdown did not appear after clicking 'More'"

            # List of dropdown elements
            try:
                options = [
                    main_page.wait.until(lambda d: d.find_element(*main_page.faq_locator)),
                    main_page.wait.until(lambda d: d.find_element(*main_page.blog_locator)),
                    main_page.wait.until(lambda d: d.find_element(*main_page.careers_locator))
                ]
            except TimeoutException:
                pytest.fail("One or more dropdown options were not found")

            # Hover over each option and assert it gets highlighted
            for option in options:
                ActionChains(driver).move_to_element(option).perform()

                # Check highlighting via CSS background-color (or class name change)
                bg_color = option.value_of_css_property("background-color")
                assert bg_color != "rgba(0, 0, 0, 0)" and bg_color is not None, f"{option.text} is not highlighted"

        else:
            pytest.skip("'More' button does not exist, skipping dropdown hover test")

# Negative Tests
# ----------------------------

    def test_home_url_negative(self, driver):
        """Negative test: assert wrong URL should fail (expected)"""
        main_page = MainPage(driver)
        wrong_url = "https://wrong-url.org/"

        # This will pass if wrong_url is NOT in the actual URL
        assert wrong_url not in main_page.get_url(), "Negative test passed: wrong URL is not present"

    def test_nav_menu_items_negative(driver):
        """Negative test: verify nav menu items with wrong locators are not found"""
        main_page = MainPage(driver)
        wrong_locators = main_page.negative_nav_data()

        for name, locator in wrong_locators.items():
            try:
                # Try to find element with wrong locator
                main_page.wait.until(lambda d: d.find_element(*locator))
                # If found, test should fail
                assert False, f"Negative test failed: '{name}' element was unexpectedly found"
            except:
                # Expected path: element not found
                assert True
