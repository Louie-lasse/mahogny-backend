from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os

class Scraper():

    FIREFOX_BINARY = os.path.abspath("app/firefox/firefox-bin")
    GECKODRIVER_PATH = os.path.abspath("app/geckodriver")

    def __init__(self) -> None:
        self._driver = self._create_selenium_driver()
    
    def _create_selenium_driver(self):
        """
        Create a new Selenium driver instance.
        """
        options = Options()
        options.binary_location = self.FIREFOX_BINARY
        options.add_argument("--headless")
        service = FirefoxService(executable_path=self.GECKODRIVER_PATH)
        driver = webdriver.Firefox(service=service, options=options)
        return driver
    
    async def login(self, user, password):
        self._driver.get("https://www.chalmersstudentbostader.se/login")
        print("Navigated to login page")
        # Perform login actions
        self._driver.find_element(By.ID, 'user_login').send_keys(user)
        self._driver.find_element(By.ID, 'user_pass').send_keys(password)
        print("Filled in login details")
        self._driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()

        wait = WebDriverWait(self._driver, 10)  # Waits up to 10 seconds
        element = wait.until(EC.presence_of_element_located((By.XPATH, "//a[text()='Boka']")))

        self._driver.get(element.get_attribute("href"))
        
        print("logged in")
        return True
    
    def __exit__(self, exc_type, exc_value, traceback):
        self._driver.quit()
