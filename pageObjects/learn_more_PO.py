from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class LearnMorePO:
    """Page Object for the Learn more page"""

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 2)  # 2-second wait for every interaction

    # Attributes / Locators
    learn_more_locator = (By.CSS_SELECTOR, 'div[class="MuiGrid2-root MuiGrid2-direction-xs-row MuiGrid2-grid-xs-12 '
                                           'mui-414w8z"] div button')
    express_interest = (By.CSS_SELECTOR, "h3[class='MuiTypography-root MuiTypography-h3 mui-cp2isa']")
    provider_option = (By.XPATH, "//h6[text()='Provider']")
    employer_option = (By.XPATH, "//h6[text()='Employer']")
    tpa_option = (By.XPATH, "//h6[text()='TPA']")
    next_button = (By.XPATH, "//button[text()='Next']")

    #proviers autofill-locators
    email_field = (By.CSS_SELECTOR, "div[class='MuiFormControl-root MuiFormControl-fullWidth MuiTextField-root "
                                    "mui-1i1xszt'] div input")
    form_fields = (By.CSS_SELECTOR, "div[class='MuiFormControl-root MuiFormControl-fullWidth "
                                         "MuiTextField-root mui-94mdxe']")

    # methods
    def fill_form(self, email, first_name, last_name, company_name):
        """
        Auto-fills the provider form.
        Email has a unique selector, the rest share a common one.
        """
        try:
            # Fill email first
            email_input = self.wait.until(EC.presence_of_element_located(self.email_field))
            email_input.click()
            email_input.send_keys(email)

            # Fill the rest of the fields
            fields = self.wait.until(EC.presence_of_all_elements_located(self.form_fields))

            if len(fields) < 3:
                raise Exception("Not all form fields were found on the page.")

            # Enter first name, last name, company in order
            fields[0].click()
            fields[0].find_element(By.TAG_NAME, "input").send_keys(first_name)

            fields[1].click()
            fields[1].find_element(By.TAG_NAME, "input").send_keys(last_name)

            fields[2].click()
            fields[2].find_element(By.TAG_NAME, "input").send_keys(company_name)

        except TimeoutException:
            raise Exception("Form fields not found for auto-filling.")

    def click_provider(self):
        self.driver.find_element(*self.provider_option).click()
        self.driver.find_element(*self.next_button).click()

    def does_provider_exist(self):
        provider = self.driver.find_element(*self.provider_option)
        return provider.is_displayed()

    def is_learn_more_present(self):
        try:
            element = self.wait.until(EC.visibility_of_element_located(self.learn_more_locator))
            return element.is_displayed()
        except TimeoutException:
            return False

    def scroll_to(self, locator):
        """
        Scroll the page until the element specified by `locator` is in view.
        `locator` should be a tuple, e.g., (By.CSS_SELECTOR, "button#id")
        """
        try:
            element = self.wait.until(EC.presence_of_element_located(locator))
            self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", element)
            return element  # Return the element in case further actions are needed
        except TimeoutException:
            raise Exception(f"Element with locator {locator} was not found for scrolling.")

    def click_learn_more(self):
        """Clicks the Learn More button and waits for next page to load"""
        self.scroll_to(self.learn_more_locator)
        self.wait.until(EC.element_to_be_clickable(self.learn_more_locator)).click()
        self.wait.until(EC.visibility_of_element_located(self.express_interest))
