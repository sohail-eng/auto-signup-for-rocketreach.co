from time import sleep

from .file_operations import get_account_limit, get_initial_link, get_sleep_seconds
from .rocket_reach import RocketReach


def fill_data_into_rocket_reach(data: list, driver):
    processed_list = []
    un_successful_list = []

    breaker = None
    breaker_username = None
    breaker_email = None

    account_length = get_account_limit()
    initial_link = get_initial_link()
    sleep_seconds = get_sleep_seconds()

    try:
        try:
            driver.get(initial_link)
        except Exception as e:
            print(e)
        j = RocketReach(proxy='', driver=driver)
        counter = 0
        for username, email in data:
            sleep(sleep_seconds)
            counter = counter + 1
            if counter > account_length:
                counter = 0
                j.driver.close()
                j = RocketReach()
                try:
                    j.driver.get(initial_link)
                except Exception as e:
                    print(e)
            if j.fill_information(
                username=username,
                email=email,
                password=email
            ):
                if j.no_browser:
                    breaker = True
                    breaker_username = username
                    breaker_email = email
                    break
                processed_list.append([username, email])
            else:
                un_successful_list.append([username, email])
    except (Exception) as e:
        print(e)
        pass
    if breaker:
        un_successful_list.append([breaker_username, breaker_email])
    return processed_list, un_successful_list
