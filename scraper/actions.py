import getpass
import os
import pickle
from time import sleep

from selenium.common import NoSuchElementException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By

from .constants import (
    VERIFY_LOGIN_ID,
    COOKIE_FILE_NAME,
    REMEMBER_PROMPT
)

BASE_URL = "https://www.linkedin.com/"


def page_has_loaded(driver):
    page_state = driver.execute_script('return document.readyState;')
    return page_state == 'complete'


def action_click(driver, element):
    action = ActionChains(driver)
    action.click(element)
    action.perform()
