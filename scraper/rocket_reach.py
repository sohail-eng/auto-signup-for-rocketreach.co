import logging

from selenium.webdriver.common.by import By

from .actions import action_click
from .objects import Scraper

logging.basicConfig()


class RocketReach(Scraper):
    first_name = ""
    last_name = ""
    location = ""
    company_name = ""
    keywords = ""

    def __init__(
            self,
            driver=None,
            proxy=None
    ):
        self.driver = driver
        self.base_url = "https://rocketreach.co/"

        self.sign_up_url = f"{self.base_url}signup?next=%2F"
        self.logout_link = f"{self.base_url}/logout"

        if not self.driver:
            self.driver = self.initialize(proxy=proxy)
            self.driver.get(self.base_url)

    def fill_information(
            self,
            username: str = "",
            email: str = "",
            password: str = "",
            delay: int = 30,
    ):
        try:
            self.driver.get(self.sign_up_url)
            self.wait(3)
            self.get_elements_by_time(
                by=By.XPATH,
                value='//input[@id="name"]'
            ).send_keys(username)
            self.get_elements_by_time(
                by=By.XPATH,
                value='//input[@id="email"]'
            ).send_keys(email)
            self.get_elements_by_time(
                by=By.XPATH,
                value='//input[@id="password"]'
            ).send_keys(password)
            self.get_elements_by_time(
                by=By.XPATH,
                value='//input[@id="password"]'
            ).submit()

            self.wait(delay)

            for _ in range(4):

                self.click_button(
                    element=self.get_elements_by_time(
                        by=By.XPATH,
                        value='//button[contains(@class,"next")]'
                    )
                )
                self.wait(5)

            self.driver.get(self.logout_link)
            self.wait(10)
            return True

        except Exception as e:
            print(e)
            return False
