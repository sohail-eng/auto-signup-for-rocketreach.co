import logging

from pynput.keyboard import Key, Controller

from selenium.webdriver.common.by import By

from .objects import Scraper

from selenium.common.exceptions import NoSuchWindowException

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
        self.no_browser = None
        self.driver = driver
        self.base_url = "https://rocketreach.co/"

        self.sign_up_url = f"{self.base_url}signup?next=%2F"
        self.profile_link = f"{self.base_url}person"
        self.logout_link = f"{self.base_url}logout"
        self.login_url = f"{self.base_url}login"

        self.error_email = False

        if not self.driver:
            self.driver = self.initialize(proxy=proxy)

    def fill_information(
            self,
            username: str = "",
            email: str = "",
            password: str = ""
    ):
        self.no_browser = None
        try:
            response = self.middle_method_for_retry(
                method_name=self.open_signup_url
            )
            if not response:
                if self.no_browser:
                    return False
                print("Failed to open signup url, Retry again")
                self.middle_method_for_retry(
                    method_name=self.successful_logout
                )
                return self.fill_information(
                    username=username,
                    email=email,
                    password=password
                )

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

            response = self.middle_method_for_retry(
                method_name=self.signup_successful_or_error
            )

            if not response:
                if self.no_browser:
                    return False
                if self.error_email:
                    print("Email Already Exist")
                    return False
                print("Failed to signup, Retry again")
                self.middle_method_for_retry(
                    method_name=self.successful_logout
                )
                response = self.fill_information(
                    username=username,
                    email=email,
                    password=password
                )
                if self.no_browser:
                    return False
                return response

            self.focus()

            self.get_elements_by_time(
                by=By.XPATH,
                value='//button[contains(@class,"next")]',
                seconds=15,
                single=True
            )

            keyboard = Controller()
            keyboard.press(Key.enter)
            keyboard.release(Key.enter)

            self.wait(10)

            return self.middle_method_for_retry(
                method_name=self.successful_logout
            )
        except NoSuchWindowException as e:
            self.no_browser = True
            print(e)
            return False

        except Exception as e:
            print(e)
            return False

    def signup_successful_or_error(self, **kwargs):
        self.get_elements_by_time(
            by=By.XPATH,
            value='//input[@id="password"]'
        ).submit()
        inner_count = 0
        self.error_email = False
        while True:
            if self.driver.current_url.split("?")[0] == self.profile_link.split("?")[0]:
                return True
            if self.get_elements_by_time(
                by=By.XPATH,
                value='//li[@class="ng-binding"]',
                seconds=1
            ):
                self.error_email = True
                return False
            inner_count = inner_count + 1
            if inner_count > 60:
                break
        return False


    def open_signup_url(self, **kwargs):
        self.driver.get(self.sign_up_url)
        inner_count = 0
        while True:
            if self.driver.current_url.split("?")[0] == self.sign_up_url.split("?")[0]:
                element = self.get_elements_by_time(
                    by=By.XPATH,
                    value='//input[@id="name"]'
                )
                if element:
                    return True
            self.wait(1)
            inner_count = inner_count + 1
            if inner_count > 60:
                break
        return False

    def successful_logout(self, **kwargs):
        self.driver.get(self.logout_link)
        inner_counter = 0
        while True:
            try:
                self.wait(1)
                if self.driver.current_url == self.login_url:
                    return True
                inner_counter = inner_counter + 1
                if inner_counter > 60:
                    break
            except NoSuchWindowException as e:
                self.no_browser = True
                print(e)
                return False
            except Exception as e:
                print(e)
                break
        return False

    def middle_method_for_retry(self, method_name, **kwargs):
        count = 0
        while count < 3:
            try:
                response = method_name(**kwargs)
                if response:
                    return True
            except NoSuchWindowException as e:
                self.no_browser = True
                print(e)
                return False
            count = count + 1
        return False
