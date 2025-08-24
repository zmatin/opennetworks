import random
import string

from selenium.common import TimeoutException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class MainPage:
    """Page Object for the Open Networks main page"""

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 2)  # 2-second wait for every interaction

    # Attributes / Locators
    logo_locator = (By.CSS_SELECTOR, 'div[class="MuiBox-root mui-w1el9g"]')
    nav_menu_home_locator = (By.CSS_SELECTOR, "button[id=':Rcrkq9nlb:']")
    nav_menu_about_us_locator = (By.CSS_SELECTOR, "button[id=':Rkrkq9nlb:']")
    nav_menu_providers_locator = (By.CSS_SELECTOR, "button[id=':Rsrkq9nlb:']")
    nav_menu_employers_locator = (By.CSS_SELECTOR, "button[id=':R14rkq9nlb:']")
    nav_menu_more_locator = (By.CSS_SELECTOR, "button[id='demo-customized-button']")
    more_dropdown_locator = (By.CSS_SELECTOR, "ul[class='MuiList-root MuiList-padding MuiMenu-list mui-ubifyk']")

    # drop_down more menu options
    faq_locator = (By.XPATH, "//li[text()='FAQ']")
    blog_locator = (By.XPATH, "//li[text()='Blog']")
    careers_locator = (By.XPATH, "//li[text()='Careers']")

    # Constants
    EXPECTED_TITLE = "OpenNetworks"
    HOME_URL = "https://opennetworks.org/"

    # Methods

    def negative_nav_data(self):
        """
        Return a dictionary of intentionally wrong nav menu locators for negative testing.
        Randomly appends a letter or number to make each call unique.
        """

        def random_suffix(length=1):
            return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

        return {
            "Home": ("CSS_SELECTOR", f"button[id=':Rcrkq9nlb:{random_suffix()}']"),
            "About Us": ("CSS_SELECTOR", f"button[id=':Rkrkq9nlb:{random_suffix()}']"),
            "Providers": ("CSS_SELECTOR", f"button[id=':Rsrkq9nlb:{random_suffix()}']"),
            "Employers": ("CSS_SELECTOR", f"button[id=':R14rkq9nlb:{random_suffix()}']")
        }

    def move_and_click_more(self):
        """Move to the More button, click it, and verify dropdown appears"""
        try:
            # Wait for the More button
            more_button = WebDriverWait(self.driver, 2).until(
                EC.element_to_be_clickable(self.nav_menu_more_locator)
            )

            # Move to the button and click
            ActionChains(self.driver).move_to_element(more_button).click().perform()

            # Wait for the dropdown to appear
            dropdown = WebDriverWait(self.driver, 2).until(
                EC.visibility_of_element_located(self.more_dropdown_locator)
            )
            return True  # Dropdown appeared
        except TimeoutException:
            return False  # Either button or dropdown not found

    def man_menu_more(self):
        """Return the 'More' menu element, waits up to 2 seconds"""
        return self.wait.until(EC.presence_of_element_located(self.nav_menu_more_locator))

    def does_nav_more_button_exist(self):
        """Check if the 'More' menu button exists"""
        try:
            self.man_menu_more()
            return True
        except TimeoutException:
            return False

    def title_page(self):
        """Return the current page title"""
        return self.driver.title

    def get_url(self):
        """Return the current page URL"""
        return self.driver.current_url

    def page_source(self):
        """Return the full page source (HTML)"""
        return self.driver.page_source

    def nav_menu_home(self):
        return self.wait.until(EC.presence_of_element_located(self.nav_menu_home_locator))

    def nav_menu_about_us(self):
        return self.wait.until(EC.presence_of_element_located(self.nav_menu_about_us_locator))

    def nav_menu_providers(self):
        return self.wait.until(EC.presence_of_element_located(self.nav_menu_providers_locator))

    def nav_menu_employers(self):
        return self.wait.until(EC.presence_of_element_located(self.nav_menu_employers_locator))

    def click_logo(self):
        self.wait.until(EC.element_to_be_clickable(self.logo_locator)).click()

    def is_logo_present(self):
        return self.wait.until(EC.visibility_of_element_located(self.logo_locator)).is_displayed()
